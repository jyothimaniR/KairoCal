# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db, get_engine, run_migrations_if_configured, migration_status, init_engine
from app.core.metrics import record_http_request, render_prometheus
from app.config import get_settings

# Import existing routers
from app.api import users, events
try:
    from app.api import reminders
    HAS_REMINDERS = True
except ImportError:
    HAS_REMINDERS = False

import os as _os  # local alias to avoid later shadowing

# Lightweight mode flags (used by OpenAPI validation script)
_disable_nlp = _os.getenv("DISABLE_NLP", "false").lower() == "true"
_disable_analytics = _os.getenv("DISABLE_ANALYTICS", "false").lower() == "true"
_disable_conflicts = _os.getenv("DISABLE_CONFLICTS", "false").lower() == "true"

if not _disable_nlp:
    try:
        from app.api import nlp
        HAS_NLP = True
    except ImportError:
        HAS_NLP = False
else:
    HAS_NLP = False

if not _disable_analytics:
    try:
        from app.api.analytics import router as analytics_router
        HAS_ANALYTICS = True
    except ImportError:
        HAS_ANALYTICS = False
else:
    HAS_ANALYTICS = False

try:
    from app.api.conflicts import router as conflicts_router
    HAS_CONFLICTS = True
except ImportError:
    HAS_CONFLICTS = False

try:
    from app.api.voice import voice_router
    HAS_VOICE = True
except ImportError:
    HAS_VOICE = False

# NEW: Priority-based scheduling API (safe import)
try:
    from app.api.priority_api import router as priority_router
    HAS_PRIORITY_API = True
except ImportError:
    HAS_PRIORITY_API = False

# Import models to ensure they're registered with SQLAlchemy
from app.models import User, Event, Reminder

settings = get_settings()

app = FastAPI(
    title="KairoCal API",
    description="AI-Powered Smart Calendar System with BERT Priority Classification",
    version="1.0.0",
    debug=settings.app_debug
)

# Configure CORS - Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers (with safe imports)
app.include_router(users.router)
app.include_router(events.router)

if HAS_REMINDERS:
    app.include_router(reminders.router)

if HAS_NLP:
    app.include_router(nlp.router)  # BERT NLP endpoints

if HAS_ANALYTICS:
    app.include_router(analytics_router)

if HAS_CONFLICTS and not _disable_conflicts:
    app.include_router(conflicts_router)

if HAS_VOICE:
    app.include_router(voice_router)

# NEW: Include priority-based scheduling API (safe addition)
if HAS_PRIORITY_API:
    app.include_router(priority_router)

import os, logging, time, uuid, contextvars, traceback
logger = logging.getLogger(__name__)
_correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="")

_READINESS_CACHE = {"ready": False, "reason": "initializing"}

@app.on_event("startup")
def startup_db():
    try:
        init_engine()
        run_migrations_if_configured()
        ms = migration_status()
        require_sync = os.getenv("READINESS_REQUIRE_MIGRATION_SYNC", "true").lower() == "true"
        if require_sync and ms.get("status") not in ("ok",):
            _READINESS_CACHE.update({"ready": False, "reason": f"migration_status={ms.get('status')}", "migration": ms})
        else:
            _READINESS_CACHE.update({"ready": True, "reason": "ok", "migration": ms})
        logger.info("DB readiness state %s", _READINESS_CACHE)
    except Exception as e:
        _READINESS_CACHE.update({"ready": False, "reason": f"error:{e}"})
        logger.exception("Startup DB init failed")

# Request timing middleware (placed after startup for simplicity)
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    cid = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    _correlation_id_ctx.set(cid)
    start = time.time()
    slow_req_threshold = int(os.getenv("SLOW_REQUEST_THRESHOLD_MS", "500"))
    response: Response | None = None
    try:
        response = await call_next(request)
        return response
    finally:
        try:
            duration_ms = (time.time() - start) * 1000.0
            path_template = getattr(getattr(request.scope.get('route'), 'path', None), 'strip', lambda: request.url.path)()
            status_code = getattr(response, 'status_code', 500)
            record_http_request(request.method, path_template, status_code, duration_ms, slow_req_threshold)
            if duration_ms >= slow_req_threshold:
                logger.warning("SLOW_REQUEST %s %.1fms %s", request.method, duration_ms, path_template)
            if response is not None:
                try:
                    response.headers["X-Request-Id"] = cid
                except Exception:
                    pass
        except Exception as m_err:  # Never let metrics path kill request
            logger.debug("timing_middleware_finalize_error %s", m_err)

@app.middleware("http")
async def unified_error_wrapper(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as he:
        logger.warning("http_exception", extra={
            "status": he.status_code,
            "detail": he.detail,
            "path": request.url.path,
            "cid": _correlation_id_ctx.get()
        })
        return JSONResponse(
            status_code=he.status_code,
            content={
                "error": {
                    "code": he.status_code,
                    "message": he.detail,
                    "correlation_id": _correlation_id_ctx.get(),
                    "path": request.url.path
                }
            },
        )
    except Exception as e:
        tb_tail = "".join(traceback.format_exception(type(e), e, e.__traceback__))[-1500:]
        logger.error("unhandled_exception", extra={
            "exc_type": type(e).__name__,
            "error": str(e),
            "path": request.url.path,
            "cid": _correlation_id_ctx.get(),
            "trace_tail": tb_tail
        })
        debug = bool(os.getenv("DEBUG", str(settings.app_debug)).lower() == "true")
        msg = "Internal Server Error"
        if debug:
            msg = f"{type(e).__name__}: {e}"
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": 500,
                    "message": msg,
                    "correlation_id": _correlation_id_ctx.get(),
                    "path": request.url.path
                }
            },
        )

@app.get("/ready")
def readiness_probe():
    if _READINESS_CACHE.get("ready"):
        return {"ready": True, "migration": _READINESS_CACHE.get("migration")}
    raise HTTPException(status_code=503, detail=_READINESS_CACHE)

@app.get("/")
def read_root():
    features = [
        "User Management",
        "Event Scheduling", 
        "Smart Reminders"
    ]
    
    if HAS_NLP:
        features.extend([
            "🧠 BERT Priority Classification",
            "🤖 AI-Powered Event Analysis"
        ])
    
    if HAS_VOICE:
        features.extend([
            "🎤 Voice-to-Text Event Creation",
            "🗣️ Natural Language Voice Processing"
        ])
    
    if HAS_CONFLICTS:
        features.extend([
            "⚡ Smart Conflict Detection",
            "🎯 Auto-Resolution System"
        ])
    
    if HAS_PRIORITY_API:
        features.extend([
            "📅 Priority-Based Scheduling",
            "⚡ Intelligent Time Slot Suggestions"
        ])
    
    return {
        "message": "KairoCal API with BERT Priority Classification is running!",
        "status": "healthy",
        "version": "1.0.0",
        "features": features
    }

@app.get("/health")
def health_check():
    status = {
        "status": "healthy",
        "service": "kairocal-api",
        "database": "connected"
    }
    
    if HAS_NLP:
        status["bert_nlp"] = "operational"
    
    if HAS_VOICE:
        status["voice_api"] = "operational"
    
    if HAS_CONFLICTS:
        status["conflict_detection"] = "operational"
    
    if HAS_PRIORITY_API:
        status["priority_scheduling"] = "operational"
    
    return status

@app.get("/api/v1/status")
def api_status():
    features = [
        "User Management",
        "Event Scheduling", 
        "Smart Reminders"
    ]
    
    endpoints = {
        "events": "/api/v1/events",
        "users": "/api/v1/users"
    }
    
    if HAS_NLP:
        features.extend([
            "🧠 BERT Priority Classification",
            "🤖 Natural Language Processing"
        ])
        endpoints["nlp"] = "/api/v1/nlp"
    
    if HAS_VOICE:
        features.extend([
            "🎤 Voice-to-Text API",
            "🗣️ Voice Event Creation"
        ])
        endpoints["voice"] = "/api/v1/voice"
    
    if HAS_ANALYTICS:
        features.append("📊 User Behavior Analytics")
        endpoints["analytics"] = "/api/v1/analytics"
    
    if HAS_CONFLICTS:
        features.extend([
            "⚡ Smart Conflict Detection",
            "🎯 Auto-Resolution System"
        ])
        endpoints["conflicts"] = "/api/v1/conflicts"
    
    if HAS_PRIORITY_API:
        features.extend([
            "📅 Priority-Based Intelligent Scheduling",
            "⚡ Smart Time Slot Suggestions"
        ])
        endpoints["priority"] = "/api/v1/priority"
    
    return {
        "api_version": "1.0.0",
        "service": "KairoCal Backend with BERT",
        "status": "operational",
        "features": features,
    "endpoints": endpoints,
    "database_url": str(settings.database_url)
    }

@app.get("/api/v1/database/status")
def database_status(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text, inspect
        db.execute(text("SELECT 1"))
        eng = get_engine()
        inspector = inspect(eng)
        tables = inspector.get_table_names()
        ms = migration_status()
        return {
            "database_status": "connected",
            "tables_created": len(tables),
            "tables": tables,
            "migration": ms,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/v1/database/migration-status")
def migration_status_endpoint():
    return migration_status()

@app.get("/metrics")
def metrics_endpoint():
    return Response(render_prometheus(), media_type="text/plain; version=0.0.4")

# Demo endpoint to showcase BERT capabilities (only if NLP is available)
if HAS_NLP:
    @app.get("/api/v1/demo/bert-features")
    def demo_bert_features():
        """Showcase the BERT priority classification capabilities"""
        return {
            "bert_priority_classification": {
                "features": [
                    "Semantic understanding of event text",
                    "Multi-dimensional feature analysis",
                    "Temporal context encoding", 
                    "Location-aware classification",
                    "Confidence scoring",
                    "Fallback to keyword-based system"
                ],
                "priority_levels": {
                    "1": "Very Low (coffee breaks, optional events)",
                    "2": "Low (casual meetings, personal time)",
                    "3": "Medium (regular meetings, standard work)",
                    "4": "High (important presentations, client meetings)",
                    "5": "Critical (urgent CEO meetings, emergencies)"
                }
            },
            "api_endpoints": [
                "POST /api/v1/nlp/predict-priority - Get priority prediction",
                "POST /api/v1/nlp/explain-priority - Get detailed explanation",
                "POST /api/v1/nlp/batch-predict - Batch processing",
                "GET /api/v1/nlp/model-status - Check BERT model status"
            ],
            "integration": {
                "conflict_detection": "Enhanced priority-based conflict resolution",
                "event_creation": "Automatic priority assignment during event creation",
                "user_analytics": "Priority patterns analysis for better suggestions"
            }
        }

# Demo endpoint to showcase Voice API capabilities (only if Voice is available)
if HAS_VOICE:
    @app.get("/api/v1/demo/voice-features")
    def demo_voice_features():
        """Showcase the Voice-to-Text API capabilities"""
        return {
            "voice_to_text_processing": {
                "features": [
                    "Voice text cleaning and normalization",
                    "Filler word removal (um, uh, like, etc.)",
                    "Voice-specific pattern recognition",
                    "Natural language entity extraction",
                    "Real-time event creation from voice",
                    "Full BERT integration for priority classification"
                ],
                "supported_commands": {
                    "meeting_scheduling": [
                        "Schedule meeting with John tomorrow at 3pm",
                        "Set up board meeting next Friday morning"
                    ],
                    "appointment_booking": [
                        "Book doctor appointment next Tuesday at 2pm",
                        "Remind me to call dentist tomorrow"
                    ],
                    "urgent_events": [
                        "URGENT: Emergency team meeting now",
                        "ASAP: Client call about contract issues"
                    ],
                    "casual_events": [
                        "Coffee break in 30 minutes",
                        "Lunch with team next Friday"
                    ]
                }
            },
            "api_endpoints": [
                "POST /api/v1/voice/transcribe - Clean and process voice text",
                "POST /api/v1/voice/create-event - Create event from voice input",
                "POST /api/v1/voice/analyze-voice - Analyze voice without creating event",
                "GET /api/v1/voice/health - Check voice API status"
            ],
            "integration": {
                "bert_classification": "Automatic priority detection from voice",
                "nlp_processing": "Advanced entity extraction and parsing",
                "event_creation": "Seamless voice-to-calendar integration",
                "confidence_scoring": "Reliability assessment for voice commands"
            },
            "example_curl": {
                "create_event": 'curl -X POST "http://localhost:8000/api/v1/voice/create-event" -H "Content-Type: application/json" -d \'{"voice_text": "Schedule urgent client meeting tomorrow at 2pm", "user_id": 1}\'',
                "analyze_voice": 'curl -X POST "http://localhost:8000/api/v1/voice/analyze-voice" -d "voice_text=Coffee with team next week&user_id=1"'
            }
        }