# KairoCal Database Reference (Current Setup)

_Last updated: 2025-08-09_

This document is the authoritative reference for the KairoCal backend database architecture, configuration, operations, observability, and troubleshooting. It is intended to enable any engineer (new or experienced) to understand, operate, and evolve the database layer safely.

---
## 1. Database Architecture Overview

**Primary Store:** PostgreSQL 15 (containerized via `postgres:15-alpine`).  
**Fallbacks:** None. SQLite support and all implicit table-creation shortcuts have been removed to eliminate schema drift and hidden production parity risks.

**Connection Lifecycle:**
- Engine initialized lazily on first dependency use or at app startup (`init_engine()` in `backend/app/core/database.py`).
- Connection pool created once; reused globally.
- Session management is handled via FastAPI dependency `get_db()` which ensures commit/rollback and close semantics per request.

**Pooling & Resilience:**
- SQLAlchemy 2.0 engine with explicit pool sizing.
- `pool_pre_ping=True` ensures dead connections are recycled.
- Statement timeout + UTC timezone set per new DBAPI connection.
- Connection retry logic with exponential backoff sequence: `[1,2,5,10,20]` seconds (see `DEFAULT_BACKOFF`). Fails fast after exhausting attempts and surfaces last error.

**Environment-Specific Behavior:**
- Dev / local: `AUTO_MIGRATE=true` (default) applies migrations automatically at startup.
- Prod recommendation: Set `AUTO_MIGRATE=false` and run migrations through CI/CD pipeline (manual or orchestrated) to avoid unexpected runtime schema changes.
- Readiness gating controlled by `READINESS_REQUIRE_MIGRATION_SYNC` (default `true`). In production you generally keep this `true` to ensure traffic isn't routed before schema compatibility.

---
## 2. Connection Configuration

**Engine Initialization Code Reference:** `backend/app/core/database.py::init_engine()`

**DATABASE_URL Format:**
```
postgresql://<user>:<password>@<host>:<port>/<database>
```
Examples:
```
postgresql://kairocal_user:Test123@localhost:5432/kairocal
postgresql://kairocal_user:Test123@postgres:5432/kairocal   # inside docker-compose network
```

**Pooling Parameters (all configurable via env vars):**
| Setting | Env Var | Default | Description |
|---------|---------|---------|-------------|
| pool_size | `DB_POOL_SIZE` | 10 | Base size of the connection pool |
| max_overflow | `DB_MAX_OVERFLOW` | 5 | Extra transient connections allowed |
| pool_timeout | `DB_POOL_TIMEOUT` | 30 | Seconds to wait for a free connection before error |
| pool_recycle | hard-coded | 1800 | Recycles connections after 30 minutes to avoid stale sessions |
| pre_ping | enabled | n/a | Validates connection liveness before use |

**Statement Timeout:**
- Env var: `STATEMENT_TIMEOUT_MS` (default `5000`).
- Implemented in `init_engine()` via a per-connection callback: `SET statement_timeout TO <ms>` and `SET TIME ZONE 'UTC'`.
- Prevents runaway queries from degrading service quality.

**Additional DB Env Vars:** see Section 9.

**Security of URL:**
- Masked in logs via `_mask_db_url()` to avoid password leakage (`user:***@host`).

---
## 3. Migration System (Alembic)

**Tooling:** Alembic `1.12.x` configured via `backend/alembic.ini` (mounted/available at runtime as `/app/alembic.ini`).

**Key Functions:**
- `run_migrations_if_configured()` – applies `alembic upgrade head` when `AUTO_MIGRATE=true`.
- `migration_status()` – inspects DB and migration scripts to classify status.

**Status Values:**
| Status | Meaning |
|--------|---------|
| `ok` | Current DB revision matches head |
| `pending` | DB revision behind head (or version table absent) |
| `diverged` | DB revision not in current migration graph |
| `unknown` | Error determining status |

**Startup Flow:**
1. `init_engine()` connects to DB.
2. If `AUTO_MIGRATE=true` → `run_migrations_if_configured()` executes `upgrade head`.
3. `migration_status()` runs and readiness cache updated.

**File Locations:**
- Alembic env script: `backend/alembic/env.py`
- Alembic configuration: `backend/alembic.ini` (referenced via helper `_alembic_ini_path()`).
- Migration versions directory: `backend/alembic/versions/` (ensure new revisions saved here).

**Checking Status Manually:**
```bash
alembic current
alembic heads
alembic history --verbose | tail -n 20
```
(Needs `DATABASE_URL` exported.)

---
## 4. Health & Monitoring Endpoints

| Endpoint | Path | Behavior |
|----------|------|----------|
| Liveness (conceptual) | `/` or `/health` | Basic service response & static subsystem flags |
| Readiness | `/ready` | 200 only if DB reachable & (optionally) migrations in sync; else 503 with reason |
| DB Status | `/api/v1/database/status` | Executes `SELECT 1`, lists tables, includes migration status |
| Migration Status | `/api/v1/database/migration-status` | Raw `migration_status()` JSON |
| Metrics | `/metrics` | Prometheus text exposition of HTTP & DB metrics |

**/ready Logic:**
- If `READINESS_REQUIRE_MIGRATION_SYNC=true` and migrations not `ok` → 503.
- Otherwise returns 200 with current migration metadata.

---
## 5. Database Schema

Defined in `backend/app/models/` using SQLAlchemy ORM with a shared base `BaseModel`.

### 5.1 Shared Base (BaseModel)
File: `backend/app/models/__init__.py`
| Column | Type | Attributes |
|--------|------|------------|
| id | GUID (UUID native) | PK, default uuid4 |
| created_at | TIMESTAMP WITH TIME ZONE | server_default=now(), not null |
| updated_at | TIMESTAMP WITH TIME ZONE | auto-updated via `onupdate=func.now()` |

GUID type uses PostgreSQL native UUID when available.

### 5.2 Users Table (`users`)
File: `backend/app/models/user.py`
| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| id | UUID | PK |
| created_at | timestamptz | audit |
| updated_at | timestamptz | audit |
| cognito_sub | varchar(255) | unique, indexed, not null |
| email | varchar(255) | unique, indexed, not null |
| full_name | varchar(255) | nullable |
| preferences | JSON | defaults to `{}` |
| is_active | boolean | default true, not null |

Relationships:
- `events` (one-to-many) cascade delete orphan events.

### 5.3 Events Table (`events`)
File: `backend/app/models/event.py`
| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| id | UUID | PK |
| user_id | UUID | FK → users.id, indexed, not null |
| title | varchar(255) | not null |
| description | text | nullable |
| start_time | timestamptz | indexed, not null |
| end_time | timestamptz | indexed, not null |
| is_all_day | boolean | default false, not null |
| location | varchar(255) | nullable |
| recurrence_rule | varchar(255) | nullable |
| priority_level | integer | default 3 (1–5 scale) |
| priority_confidence | float | default 0.0 |
| classification_method | varchar(50) | default 'manual' |
| meeting_outcome | varchar(50) | default 'neutral' |
| effectiveness_rating | integer | default 3 |
| energy_level | integer | default 3 |
| created_via | varchar(20) | default 'manual' |
| actual_duration | integer | nullable (minutes) |
| planned_duration | integer | nullable (minutes) |
| created_at | timestamptz | audit |
| updated_at | timestamptz | audit |

Relationships:
- `user` back_populates users.events
- `reminders` one-to-many cascade delete orphan reminders

### 5.4 Reminders Table (`reminders`)
File: `backend/app/models/reminder.py`
| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| id | UUID | PK |
| event_id | UUID | FK → events.id, indexed, not null |
| minutes_before | integer | not null |
| notification_type | varchar(50) | default 'in_app' |
| is_sent | boolean | default false, not null |
| created_at | timestamptz | audit |
| updated_at | timestamptz | audit |

Relationships:
- `event` back_populates events.reminders

### 5.5 Alembic Version Table (`alembic_version`)
| Column | Type | Notes |
|--------|------|-------|
| version_num | varchar | Current schema revision |

### 5.6 Indexes & Constraints Summary
- Automatic PK indexes on UUID primary keys.
- Explicit indexes: `users.cognito_sub`, `users.email`, `events.user_id`, `events.start_time`, `events.end_time`, `reminders.event_id`.
- Foreign keys enforce referential integrity with cascading deletes (via ORM relationships + `delete-orphan`).

---
## 6. Observability & Performance

**Structured Logging:**
- JSON structured events emitted via `_json_log()` with fields like `event`, `attempt`, `duration_ms`, `sql`.
- Sensitive DB credentials masked.

**Slow Query Detection:**
- Threshold: `SLOW_QUERY_THRESHOLD_MS` (default 200 ms).
- Instrumentation: SQLAlchemy event listeners (`before_cursor_execute` / `after_cursor_execute`).
- Logs event: `{ "event": "slow_query", "duration_ms": <float>, "sql": <abbreviated> }`.

**Request Timing:**
- Middleware in `backend/app/main.py` records per-request duration.
- Slow request threshold: `SLOW_REQUEST_THRESHOLD_MS` (default 500 ms) triggers warning log `SLOW_REQUEST <METHOD> <ms> <path>`.

**Metrics (Prometheus Text Format):** `/metrics`
| Metric | Type | Meaning |
|--------|------|---------|
| http_requests_total | counter | Requests grouped by method,path,status |
| http_request_duration_ms_sum/count/max | counters/gauge | Aggregate latency per method+path |
| http_slow_requests_total | counter | Requests slower than threshold |
| db_queries_total | counter | Total SQL statements executed |
| db_slow_queries_total | counter | Queries slower than threshold |
| db_slow_query_fingerprint_total | counter | Count per slow query fingerprint (top 50) |

**Alerting Recommendations:**
- Page on sustained increase in `http_slow_requests_total / http_requests_total` > 5% over 5m.
- Investigate if `db_slow_queries_total` growth accelerates or specific fingerprint dominates.
- Track p95 latency by adding histograms (future enhancement).

---
## 7. Docker Setup

**Compose File:** `docker-compose.yml`

Services:
- `postgres`: Exposes 5432, health check using `pg_isready`, persisting data in `postgres_data` volume.
- `redis`: Ancillary cache / future use (not yet deeply integrated into DB flows).
- `backend`: Waits on healthy Postgres before start, binds source code directory for live reload, exposes 8000.

**Volumes:**
- `postgres_data` → `/var/lib/postgresql/data`
- `redis_data` → `/data`
- Code mount: `./backend/app:/app/app` (enables `--reload` but not recommended for prod images).

**Network:**
- Bridge network `kairocal-network` for internal service DNS (`postgres`, `redis`).

**Security Notes:**
- Default credentials stored in compose file – acceptable for local dev only. For production use secrets manager / env injection.

**Health Dependency:**
- `depends_on.postgres.condition: service_healthy` ensures backend starts only after Postgres readiness.

---
## 8. Troubleshooting Guide

### 8.1 Connection Issues
| Symptom | Likely Cause | Action |
|---------|--------------|--------|
| Repeated `db_connect_retry` logs then failure | Wrong credentials / host unreachable | Verify `DATABASE_URL`, check container DNS (`docker exec kairocal_backend ping postgres`) |
| Immediate `db_connect_fatal` | Invalid URL scheme / missing driver | Ensure URL starts with `postgresql://` |
| Random OperationalError mid-traffic | Idle timeout / network drop | Pool pre_ping already mitigates; inspect Postgres logs |

### 8.2 Migration Problems
| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| `/ready` 503 with `pending` | DB behind head | Run `alembic upgrade head` or enable `AUTO_MIGRATE` |
| Status `diverged` | Revision not in graph | Identify stray revision: `alembic history`; rebase or stamp correct head: `alembic stamp <rev>` then upgrade |
| Status `unknown` | Exception encountered | Check logs for `migration_status_error`; verify path `/app/alembic.ini` exists |

### 8.3 Health Check Failures
- `/health` failing DB portion: check logs for `db_connect_retry` or `db_connect_exhausted`.
- `/ready` failing due to migration: ensure migrations directory mounted and accessible.

### 8.4 Performance Debugging
1. Inspect `/metrics` for rising `db_slow_queries_total`.
2. Identify fingerprints; correlate with application endpoints (enable verbose SQL logging temporarily: set `DEBUG=true`).
3. Use `EXPLAIN (ANALYZE, BUFFERS)` inside psql for problematic SQL.
4. Consider adding indices or rewriting query; adjust `STATEMENT_TIMEOUT_MS` only after root cause found.

### 8.5 Log Analysis Tips
- Filter JSON logs by `event` field (e.g., grep `slow_query`).
- For Kubernetes: add loki / fluent-bit pipeline to index `event` key.

### 8.6 Reset / Clean Database (DEV ONLY)
```bash
docker compose down -v  # removes volumes
docker compose up -d --build
alembic upgrade head
```

---
## 9. Environment Variables Reference

| Variable | Default (dev) | Required | Purpose | Recommendation (prod) |
|----------|---------------|----------|---------|-----------------------|
| `DATABASE_URL` | (see compose) | YES | DB connection string | Provide via secret manager; no plaintext in compose |
| `AUTO_MIGRATE` | `true` | NO | Auto-run migrations on startup | Set `false` and manage via CI/CD |
| `READINESS_REQUIRE_MIGRATION_SYNC` | `true` | NO | Gate readiness on schema sync | Keep `true` |
| `STATEMENT_TIMEOUT_MS` | `5000` | NO | Server-side per-session timeout | Tune (e.g., 3000–10000) based on workload |
| `DB_POOL_SIZE` | `10` | NO | Core pool size | Scale with concurrency & DB resources |
| `DB_MAX_OVERFLOW` | `5` | NO | Temporary extra connections | Keep modest to avoid spikes |
| `DB_POOL_TIMEOUT` | `30` | NO | Wait time for pool checkout | Adjust if transient starvation |
| `SLOW_QUERY_THRESHOLD_MS` | `200` | NO | Slow query logging/metric threshold | Start 200–500; refine with profiling |
| `SLOW_REQUEST_THRESHOLD_MS` | `500` | NO | Slow HTTP request threshold | Align with latency SLO (e.g., 95% < 500ms) |
| `DEBUG` | `true` (dev) | NO | Controls SQL echo & debug mode (through settings) | `false` in prod |

---
## 10. Development Workflows

### 10.1 Start Database Locally
```bash
docker compose up -d postgres
```
Or full stack:
```bash
docker compose up -d --build
```

### 10.2 Run Migrations Manually
```bash
export DATABASE_URL=postgresql://kairocal_user:Test123@localhost:5432/kairocal
alembic upgrade head
```

### 10.3 Check Database Status
```bash
curl http://localhost:8000/api/v1/database/status | jq
curl -i http://localhost:8000/ready
curl http://localhost:8000/metrics | head
```

### 10.4 Generate New Migration
```bash
alembic revision --autogenerate -m "add_new_feature_table"
alembic upgrade head
```
Review generated file under `backend/alembic/versions/` before applying.

### 10.5 Reset / Recreate (Dev)
```bash
docker compose down -v
rm -rf backend/app/__pycache__
docker compose up -d --build
alembic upgrade head
```

### 10.6 PSQL Access
```bash
docker exec -it kairocal_postgres psql -U kairocal_user -d kairocal
\dt
\d+ users
```

---
## 11. Production Considerations

### 11.1 Backups
- Use managed Postgres (e.g., AWS RDS) with automated daily snapshots + PITR.
- Periodic logical dumps for disaster recovery test: `pg_dump -Fc`.

### 11.2 Security
- Enforce TLS connections (require_ssl) at managed service or pg_hba rules.
- Rotate credentials; prefer IAM auth / secrets manager retrieval.
- Restrict public network exposure; only internal service network.

### 11.3 Performance Tuning
- Monitor `pg_stat_statements` (enable extension) for real slow query insight beyond fingerprints.
- Consider connection pooler (pgBouncer) if app instances scale beyond efficient direct pooling.
- Adjust pool sizes proportionally to CPU / memory on DB host.

### 11.4 Scaling
- Vertical: Increase instance size / IOPS.
- Horizontal read: Introduce read replicas for analytics or heavy read endpoints.
- Sharding: Not required yet (dataset expected moderate). Revisit if single table > tens of millions rows.

### 11.5 Future Enhancements
- Add migration drift detection in CI (generate offline SQL & compare checksum).
- Implement OpenTelemetry tracing for query spans.
- Add histogram metrics (Prometheus client) for better latency SLO enforcement.

---
## 12. Rationale Summary (WHY These Choices?)
| Decision | Why |
|----------|-----|
| Remove SQLite fallback | Prevent silent divergence & missed migrations in dev vs prod |
| Statement timeout | Guard against runaway queries harming availability |
| Pre-ping + retry | Improve resilience to transient network / startup ordering issues |
| Readiness gated by migrations | Avoid serving with incompatible schema |
| Structured JSON logs | Facilitates machine parsing & alert routing |
| In-process metrics first | Zero external deps; fast iteration; can later swap for standard client |
| Slow thresholds (200ms / 500ms) | Baseline to catch anomalies early without noise |

---
## 13. Quick Reference Commands
```bash
# Status trio
curl /ready; curl /api/v1/database/status; curl /metrics | head

# Apply migrations
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "desc"

# Investigate slow queries (psql)
SELECT now(); -- sanity
-- Enable extension once (DBA / admin):
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

---
## 14. Open Gaps / TODO
- Add automated test coverage for migration_status edge cases (divergence detection).
- Introduce query parameter redaction in slow query logs where sensitive.
- Provide formal SLO doc (availability, latency p95/p99 targets).
- Add request ID / correlation ID to logs.

---
End of document.
