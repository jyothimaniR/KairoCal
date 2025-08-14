# backend/app/core/database.py
import os
import time
import json
import logging
from typing import Optional
from sqlalchemy import create_engine, text, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config import get_settings
from app.core.metrics import record_db_query

logger = logging.getLogger(__name__)

Base = declarative_base()

_engine = None
SessionLocal: Optional[sessionmaker] = None

DEFAULT_BACKOFF = [1, 2, 5, 10, 20]  # seconds

def _json_log(level: str, **fields):
    try:
        logger.log(getattr(logging, level.upper(), logging.INFO), json.dumps(fields, default=str))
    except Exception:  # fallback
        logger.log(getattr(logging, level.upper(), logging.INFO), str(fields))

def _validate_config():
    settings = get_settings()
    url = os.getenv("DATABASE_URL", settings.database_url)
    if not url:
        raise ValueError("DATABASE_URL is required and not set")
    if not (url.startswith("postgresql") or url.startswith("sqlite")):
        raise ValueError("Only PostgreSQL and SQLite are supported")
    return url, settings

def init_engine():
    """Initialize global engine with retry & pooling. Safe to call multiple times."""
    global _engine, SessionLocal
    if _engine is not None:
        return _engine

    db_url, settings = _validate_config()
    echo = bool(settings.app_debug)
    statement_timeout_ms = int(os.getenv("STATEMENT_TIMEOUT_MS", "5000"))
    pool_size = int(os.getenv("DB_POOL_SIZE", "10"))
    max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "5"))
    pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    backoff = DEFAULT_BACKOFF

    _json_log("info", event="db_init_start", url_mask=_mask_db_url(db_url), pool_size=pool_size, max_overflow=max_overflow)

    last_error = None
    for attempt, delay in enumerate(backoff, start=1):
        try:
            eng = create_engine(
                db_url,
                echo=echo,
                future=True,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_pre_ping=True,
                pool_recycle=1800,
            )

            # Set session defaults (statement timeout, timezone) per new connection
            @event.listens_for(eng, "connect")
            def _configure_connection(dbapi_conn, _):  # pragma: no cover
                # Only configure PostgreSQL-specific settings
                if db_url.startswith("postgresql"):
                    with dbapi_conn.cursor() as cur:
                        try:
                            cur.execute(f"SET statement_timeout TO {statement_timeout_ms}")
                            cur.execute("SET TIME ZONE 'UTC'")
                        except Exception as e:  # log but don't block
                            _json_log("warning", event="db_session_config_failed", error=str(e))
                elif db_url.startswith("sqlite"):
                    # SQLite-specific configuration
                    try:
                        dbapi_conn.execute("PRAGMA foreign_keys=ON")
                        dbapi_conn.execute("PRAGMA journal_mode=WAL")
                    except Exception as e:
                        _json_log("warning", event="sqlite_config_failed", error=str(e))

            # Query timing instrumentation
            SLOW_QUERY_THRESHOLD_MS = int(os.getenv("SLOW_QUERY_THRESHOLD_MS", "200"))

            @event.listens_for(eng, "before_cursor_execute")
            def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):  # pragma: no cover
                context._query_start_time = time.time()

            @event.listens_for(eng, "after_cursor_execute")
            def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):  # pragma: no cover
                try:
                    start = getattr(context, '_query_start_time', None)
                    if start is not None:
                        dur_ms = (time.time() - start) * 1000.0
                        record_db_query(statement, dur_ms, SLOW_QUERY_THRESHOLD_MS)
                        if dur_ms >= SLOW_QUERY_THRESHOLD_MS:
                            _json_log("warning", event="slow_query", duration_ms=round(dur_ms,2), sql=_abbrev_sql(statement))
                except Exception as e:
                    _json_log("error", event="query_metrics_error", error=str(e))

            with eng.connect() as conn:
                conn.execute(text("SELECT 1"))
            _engine = eng
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
            _json_log("info", event="db_connected", attempts=attempt)
            return _engine
        except OperationalError as e:
            last_error = e
            _json_log("warning", event="db_connect_retry", attempt=attempt, delay_s=delay, error=str(e.__class__.__name__))
            time.sleep(delay)
        except Exception as e:  # Non‑recoverable
            _json_log("error", event="db_connect_fatal", error=str(e))
            raise

    _json_log("error", event="db_connect_exhausted", error=str(last_error))
    raise last_error  # bubble up

def _mask_db_url(url: str) -> str:
    try:
        # postgresql://user:pass@host:port/db -> postgresql://user:***@host:port/db
        if "@" in url and "//" in url:
            prefix, rest = url.split("//", 1)
            creds, hostpart = rest.split("@", 1)
            if ':' in creds:
                user = creds.split(':',1)[0]
                return f"{prefix}//{user}:***@{hostpart}"
        return url
    except Exception:
        return url

def _abbrev_sql(sql: str, max_len: int = 160) -> str:
    try:
        s = " ".join(sql.strip().split())
        if len(s) > max_len:
            return s[:max_len-3] + '...'
        return s
    except Exception:
        return sql[:max_len]

def get_db():
    """FastAPI dependency yielding a session."""
    if SessionLocal is None:
        init_engine()
    db = SessionLocal()  # type: ignore
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_engine():
    if _engine is None:
        return init_engine()
    return _engine

def migration_status():
    """Return (status, current_rev, head_rev). status: ok|pending|diverged|unknown"""
    from alembic.config import Config
    from alembic.script import ScriptDirectory
    from sqlalchemy import inspect
    eng = get_engine()
    try:
        cfg = Config(_alembic_ini_path())
        script = ScriptDirectory.from_config(cfg)
        head = script.get_current_head()
        with eng.connect() as conn:
            insp = inspect(conn)
            if 'alembic_version' not in insp.get_table_names():
                return {"status": "pending", "current_revision": None, "head_revision": head}
            curr = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
        if curr == head:
            return {"status": "ok", "current_revision": curr, "head_revision": head}
        if curr in {r.revision for r in script.walk_revisions()}:
            return {"status": "pending", "current_revision": curr, "head_revision": head}
        return {"status": "diverged", "current_revision": curr, "head_revision": head}
    except Exception as e:
        _json_log("error", event="migration_status_error", error=str(e))
        return {"status": "unknown", "error": str(e), "current_revision": None, "head_revision": None}

def run_migrations_if_configured():
    auto = os.getenv("AUTO_MIGRATE", "true").lower() == "true"
    if not auto:
        _json_log("info", event="migrations_skipped", auto=False)
        return
    from alembic.config import Config
    from alembic import command
    cfg = Config(_alembic_ini_path())
    try:
        command.upgrade(cfg, 'head')
        _json_log("info", event="migrations_upgraded")
    except Exception as e:
        _json_log("error", event="migrations_failed", error=str(e))
        raise

def _alembic_ini_path() -> str:
    # Always resolve to /app/alembic.ini if running in container else relative path
    candidate = "/app/alembic.ini"
    if os.path.exists(candidate):
        return candidate
    # Fallback: current file -> ../../../alembic.ini
    here = os.path.abspath(os.path.dirname(__file__))
    rel = os.path.normpath(os.path.join(here, "..", "..", "alembic.ini"))
    return rel