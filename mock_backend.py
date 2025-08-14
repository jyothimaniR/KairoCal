"""
Quick Mock Backend for Voice API Testing
Bypasses database issues to test voice endpoints
"""
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Simple mock app
app = FastAPI(title="Mock KairoCal API for Voice Testing")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Voice API models
class VoiceAnalysisRequest(BaseModel):
    voice_text: str
    user_id: Optional[str] = None
    include_bert: bool = True
    detailed_analysis: bool = False

class VoiceEventRequest(BaseModel):
    voice_text: str
    cognito_sub: str
    auto_schedule: bool = True
    priority_override: Optional[int] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Mock KairoCal API running"}

@app.get("/api/v1/status")
async def system_status():
    return {
        "status": "healthy",
        "components": {
            "bert_status": "active",
            "database": "active",
            "nlp": "active",
            "voice_api": "active"
        },
        "version": "mock-1.0.0"
    }

@app.get("/api/v1/voice/health")
async def voice_health():
    return {
        "status": "healthy",
        "voice_api": "active",
        "bert_integration": "active",
        "nlp_service": "active"
    }

@app.post("/api/v1/voice/analyze-voice")
async def analyze_voice_input(request: VoiceAnalysisRequest):
    """Mock voice analysis endpoint"""
    return {
        "bert_classification": {
            "priority": 2,
            "confidence": 0.85,
            "reasoning": "BERT classified this as high priority based on urgency indicators",
            "available": True
        },
        "nlp_analysis": {
            "keywords": ["meeting", "urgent", "tomorrow"],
            "sentiment": "neutral",
            "urgency_score": 0.8
        }
    }

@app.post("/api/v1/voice/create-event")
async def create_voice_event(request: VoiceEventRequest):
    """Mock voice event creation"""
    import uuid
    event_id = str(uuid.uuid4())
    
    return {
        "success": True,
        "event_id": event_id,
        "event_data": {
            "title": f"Voice Event: {request.voice_text[:50]}",
            "description": request.voice_text,
            "priority": 2
        },
        "bert_classification": {
            "priority": 2,
            "confidence": 0.85,
            "reasoning": "BERT analysis applied successfully"
        },
        "nlp_analysis": {
            "title": f"Voice Event: {request.voice_text[:50]}",
            "keywords": ["voice", "event"],
            "sentiment": "neutral"
        },
        "processing_details": {
            "processing_time": 0.5,
            "method": "BERT"
        },
        "message": "Event created successfully with BERT analysis"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
