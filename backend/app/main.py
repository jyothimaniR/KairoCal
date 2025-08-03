# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.config import get_settings

# Import existing routers
from app.api import users, events
try:
    from app.api import reminders
    HAS_REMINDERS = True
except ImportError:
    HAS_REMINDERS = False

try:
    from app.api import nlp
    HAS_NLP = True
except ImportError:
    HAS_NLP = False

try:
    from app.api.analytics import router as analytics_router
    HAS_ANALYTICS = True
except ImportError:
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

# Import models to ensure they're registered with SQLAlchemy
from app.models import User, Event, Reminder

settings = get_settings()

app = FastAPI(
    title="KairoCal API",
    description="AI-Powered Smart Calendar System with BERT Priority Classification",
    version="1.0.0",
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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

if HAS_CONFLICTS:
    app.include_router(conflicts_router)

if HAS_VOICE:
    app.include_router(voice_router)

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
    
    return {
        "api_version": "1.0.0",
        "service": "KairoCal Backend with BERT",
        "status": "operational",
        "features": features,
        "endpoints": endpoints
    }

@app.get("/api/v1/database/status")
def database_status(db: Session = Depends(get_db)):
    """Check database connectivity and table status"""
    try:
        from sqlalchemy import text
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        services = ["basic_api"]
        if HAS_NLP:
            services.append("bert_priority_classification")
        if HAS_VOICE:
            services.append("voice_to_text_api")
        if HAS_CONFLICTS:
            services.append("conflict_detection")
        if HAS_ANALYTICS:
            services.append("user_behavior_analytics")
        
        return {
            "database_status": "connected",
            "tables_created": len(tables),
            "tables": tables,
            "models_registered": ["users", "events", "reminders"],
            "services_operational": services
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/v1/database/create-tables")
def create_tables_endpoint():
    """Create database tables (development only)"""
    try:
        from app.core.database import Base
        Base.metadata.create_all(bind=engine)
        
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {
            "message": "Tables created successfully",
            "tables_created": tables
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Table creation failed: {str(e)}")

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