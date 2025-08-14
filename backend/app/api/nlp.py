# backend/app/api/nlp.py
"""
NLP API endpoints for BERT priority classification
Provides REST API access to the BERT-powered event priority system
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Import BERT components
try:
    from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
    from app.nlp.bert_training_data_generator import BERTTrainingDataGenerator
    from app.services.conflict_detector import SmartConflictDetector
    BERT_AVAILABLE = True
except ImportError as e:
    BERT_AVAILABLE = False
    import_error = str(e)

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/v1/nlp", tags=["NLP & BERT"])

# Global classifier instance (loaded via model_loader to support offline bundles)
_bert_classifier = None
_conflict_detector = None

def get_bert_classifier():
    """Get or initialize BERT classifier via model_loader (prefers trained local weights)."""
    global _bert_classifier
    if _bert_classifier is None and BERT_AVAILABLE:
        try:
            # Load via centralized loader to pick up backend/models path and avoid network calls
            from app.nlp.model_loader import load_bert_model
            _bert_classifier = load_bert_model()
        except Exception as e:
            logger.error(f"Failed to initialize BERT classifier: {e}")
            raise HTTPException(status_code=500, detail="BERT classifier initialization failed")
    return _bert_classifier

def get_conflict_detector():
    """Get or initialize conflict detector, pointing it at the local model path."""
    global _conflict_detector
    if _conflict_detector is None and BERT_AVAILABLE:
        try:
            from app.config import get_settings
            settings = get_settings()
            _conflict_detector = SmartConflictDetector(bert_model_path=settings.bert_model_path)
        except Exception as e:
            logger.error(f"Failed to initialize conflict detector: {e}")
            raise HTTPException(status_code=500, detail="Conflict detector initialization failed")
    return _conflict_detector

# Pydantic models
class EventData(BaseModel):
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    start_time: str = Field(..., description="Event start time (ISO format)")
    end_time: str = Field(..., description="Event end time (ISO format)")
    location: Optional[str] = Field(None, description="Event location")

class PriorityPredictionRequest(BaseModel):
    event: EventData
    user_context: Optional[Dict[str, Any]] = Field(None, description="User behavioral context")

class PriorityPredictionResponse(BaseModel):
    priority: int = Field(..., description="Priority level 1-5")
    priority_label: str = Field(..., description="Human-readable priority label")
    confidence: float = Field(..., description="Prediction confidence 0-1")
    model_used: str = Field(..., description="Model type used for prediction")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")

class BatchPredictionRequest(BaseModel):
    events: List[EventData] = Field(..., description="List of events to classify")
    user_context: Optional[Dict[str, Any]] = Field(None, description="User behavioral context")

class BatchPredictionResponse(BaseModel):
    predictions: List[PriorityPredictionResponse] = Field(..., description="List of predictions")
    total_events: int = Field(..., description="Total number of events processed")
    average_confidence: float = Field(..., description="Average confidence across all predictions")

class PriorityExplanationResponse(BaseModel):
    priority: int
    priority_label: str
    confidence: float
    reasoning: Dict[str, Any]
    feature_analysis: Dict[str, Any]

class ModelStatusResponse(BaseModel):
    bert_available: bool
    model_trained: bool
    model_info: Dict[str, Any]
    performance_stats: Dict[str, Any]

# API Endpoints
@router.get("/model-status", response_model=ModelStatusResponse)
async def get_model_status():
    """Get BERT model status and information, preferring local bundled weights."""
    if not BERT_AVAILABLE:
        return ModelStatusResponse(
            bert_available=False,
            model_trained=False,
            model_info={"error": "BERT components not available"},
            performance_stats={}
        )

    try:
        # Use model loader for accurate availability and to avoid accidental downloads
        from app.nlp.model_loader import get_model_loader
        loader = get_model_loader()
        available = loader.is_model_available()
        classifier = get_bert_classifier() if available else None
        model_info = loader.get_model_info()

        return ModelStatusResponse(
            bert_available=available,
            model_trained=bool(model_info.get("trained")) if model_info.get("loaded") else False,
            model_info=model_info,
            performance_stats={
                "fallback_mode": not bool(model_info.get("trained")),
                "confidence_threshold": 0.85
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model status: {str(e)}")

@router.post("/predict-priority", response_model=PriorityPredictionResponse)
async def predict_event_priority(request: PriorityPredictionRequest):
    """Predict priority for a single event using BERT classifier"""
    if not BERT_AVAILABLE:
        raise HTTPException(status_code=503, detail="BERT classifier not available")
    
    try:
        import time
        start_time = time.time()
        
        # Use model loader for better error handling
        from app.nlp.model_loader import load_bert_model
        classifier = load_bert_model()
        
        # Convert Pydantic model to dict
        event_data = request.event.dict()
        
        # Get prediction
        priority, confidence = classifier.predict(event_data, request.user_context)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Get priority label
        priority_labels = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
        
        return PriorityPredictionResponse(
            priority=priority,
            priority_label=priority_labels[priority],
            confidence=confidence,
            model_used="BERT" if classifier.is_trained else "Keyword-based Fallback",
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in priority prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/classify-priority")
async def classify_event_priority(event_data: dict):
    """
    Simple priority classification endpoint for direct event data
    
    Args:
        event_data: Dictionary containing event information
        
    Returns:
        Priority classification result with explanation
    """
    try:
        # Use NLP service for integrated classification
        from app.nlp.nlp_service import NLPService
        
        nlp_service = NLPService()
        priority, confidence, method = nlp_service.classify_priority(event_data)
        
        # Get priority label
        priority_labels = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
        
        return {
            "priority": priority,
            "priority_label": priority_labels.get(priority, "Unknown"),
            "confidence": confidence,
            "classification_method": method,
            "event_title": event_data.get("title", "Untitled"),
            "recommendation": _get_priority_recommendation(priority),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error in classify-priority: {e}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

def _get_priority_recommendation(priority: int) -> str:
    """Get recommendation text based on priority level"""
    recommendations = {
        1: "Low priority - can be scheduled flexibly",
        2: "Low-medium priority - schedule when convenient", 
        3: "Medium priority - standard scheduling recommended",
        4: "High priority - should be scheduled promptly",
        5: "Critical priority - requires immediate attention"
    }
    return recommendations.get(priority, "Unknown priority level")

@router.post("/batch-predict", response_model=BatchPredictionResponse)
async def batch_predict_priorities(request: BatchPredictionRequest):
    """Predict priorities for multiple events"""
    if not BERT_AVAILABLE:
        raise HTTPException(status_code=503, detail="BERT classifier not available")
    
    try:
        classifier = get_bert_classifier()
        predictions = []
        total_confidence = 0
        
        priority_labels = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
        
        for event in request.events:
            import time
            start_time = time.time()
            
            event_data = event.dict()
            priority, confidence = classifier.predict(event_data, request.user_context)
            processing_time = (time.time() - start_time) * 1000
            
            predictions.append(PriorityPredictionResponse(
                priority=priority,
                priority_label=priority_labels[priority],
                confidence=confidence,
                model_used="BERT" if classifier.is_trained else "Keyword-based Fallback",
                processing_time_ms=processing_time
            ))
            
            total_confidence += confidence
        
        average_confidence = total_confidence / len(predictions) if predictions else 0
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_events=len(request.events),
            average_confidence=average_confidence
        )
        
    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@router.post("/explain-priority", response_model=PriorityExplanationResponse)
async def explain_priority_decision(request: PriorityPredictionRequest):
    """Get detailed explanation for priority classification decision"""
    if not BERT_AVAILABLE:
        raise HTTPException(status_code=503, detail="BERT classifier not available")
    
    try:
        classifier = get_bert_classifier()
        event_data = request.event.dict()
        
        # Get explanation
        explanation = classifier.explain_prediction(event_data)
        
        # Add feature analysis
        feature_analysis = {
            "text_features": f"Analyzed title: '{event_data.get('title', '')}' and description",
            "temporal_features": f"Event time: {event_data.get('start_time', 'Not specified')}",
            "location_features": f"Location: {event_data.get('location', 'Not specified')}",
            "content_analysis": "Extracted urgency, formality, and context indicators"
        }
        
        return PriorityExplanationResponse(
            priority=explanation["priority"],
            priority_label=explanation["priority_label"],
            confidence=explanation["confidence"],
            reasoning=explanation["reasoning"],
            feature_analysis=feature_analysis
        )
        
    except Exception as e:
        logger.error(f"Error in priority explanation: {e}")
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")

@router.post("/detect-conflicts")
async def detect_scheduling_conflicts(
    new_event: EventData,
    user_id: str,
    user_context: Optional[Dict[str, Any]] = None
):
    """Detect conflicts for a new event using BERT-enhanced conflict detection"""
    if not BERT_AVAILABLE:
        raise HTTPException(status_code=503, detail="Conflict detector not available")
    
    try:
        detector = get_conflict_detector()
        
        # Mock user object (in real implementation, fetch from database)
        class MockUser:
            def __init__(self, user_id):
                self.id = user_id
                
        user = MockUser(user_id)
        event_data = new_event.dict()
        
        # Detect conflicts
        conflicts = detector.detect_conflicts(user, event_data)
        
        # Get resolution suggestions
        resolution_suggestions = detector.get_conflict_resolution_suggestions(conflicts)
        
        return {
            "conflicts_detected": len(conflicts) > 0,
            "conflict_count": len(conflicts),
            "conflicts": [
                {
                    "type": c.conflict_type.value,
                    "severity": c.severity.value,
                    "description": c.description,
                    "impact_score": c.impact_score,
                    "confidence": c.confidence,
                    "suggestions": c.suggested_resolutions
                } for c in conflicts
            ],
            "resolution_suggestions": resolution_suggestions
        }
        
    except Exception as e:
        logger.error(f"Error in conflict detection: {e}")
        raise HTTPException(status_code=500, detail=f"Conflict detection failed: {str(e)}")

# Demo endpoints for showcase
@router.get("/demo/sample-predictions")
async def demo_sample_predictions():
    """Demo endpoint showing sample BERT predictions"""
    if not BERT_AVAILABLE:
        return {"error": "BERT not available", "samples": []}
    
    try:
        classifier = get_bert_classifier()
        
        sample_events = [
            {
                "title": "URGENT: CEO Emergency Meeting",
                "description": "Critical business decision required",
                "start_time": "2025-07-30T14:00:00",
                "end_time": "2025-07-30T15:00:00",
                "location": "Executive Boardroom"
            },
            {
                "title": "Team Coffee Break",
                "description": "Casual team gathering",
                "start_time": "2025-07-30T15:30:00",
                "end_time": "2025-07-30T15:45:00",
                "location": "Office Kitchen"
            },
            {
                "title": "Client Presentation",
                "description": "Important quarterly review",
                "start_time": "2025-07-31T10:00:00",
                "end_time": "2025-07-31T12:00:00",
                "location": "Conference Room A"
            }
        ]
        
        predictions = []
        for event in sample_events:
            priority, confidence = classifier.predict(event)
            priority_labels = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
            
            predictions.append({
                "event": event,
                "priority": priority,
                "priority_label": priority_labels[priority],
                "confidence": confidence,
                "model_used": "BERT" if classifier.is_trained else "Keyword-based Fallback"
            })
        
        return {
            "sample_predictions": predictions,
            "model_status": {
                "trained": classifier.is_trained,
                "device": str(classifier.device)
            }
        }
        
    except Exception as e:
        return {"error": f"Demo failed: {str(e)}", "samples": []}

@router.get("/demo/features")
async def demo_bert_features():
    """Demo endpoint showcasing BERT classifier features"""
    return {
        "bert_priority_classification": {
            "features": [
                "🧠 Semantic understanding of event text using DistilBERT",
                "⏰ Temporal context analysis (time, urgency, duration)",
                "📍 Location-aware classification (office, remote, personal)",
                "🎯 Multi-dimensional feature extraction (64 features)",
                "📊 Confidence scoring with fallback system",
                "🔄 Real-time prediction with <100ms response time"
            ],
            "priority_levels": {
                "5": "Critical (CEO meetings, emergencies, system outages)",
                "4": "High (important presentations, client meetings)",
                "3": "Medium (regular meetings, team syncs)",
                "2": "Low (casual lunches, personal appointments)",
                "1": "Very Low (coffee breaks, optional events)"
            },
            "technical_specs": {
                "model": "DistilBERT + Custom Classification Head",
                "input_features": "Text + Temporal + Location + Content",
                "training_data": "2000+ synthetic examples per priority level",
                "accuracy_target": ">85% on validation set"
            }
        },
        "api_endpoints": [
            "POST /api/v1/nlp/predict-priority - Single event classification",
            "POST /api/v1/nlp/batch-predict - Multiple event processing",
            "POST /api/v1/nlp/explain-priority - Detailed decision explanation",
            "POST /api/v1/nlp/detect-conflicts - BERT-enhanced conflict detection",
            "GET /api/v1/nlp/model-status - Model health and status"
        ],
        "integration_points": {
            "conflict_detection": "Enhanced priority-based conflict resolution",
            "event_creation": "Automatic priority assignment during scheduling",
            "user_analytics": "Priority patterns analysis for recommendations"
        }
    }

# Error handler for BERT unavailability
@router.get("/health")
async def nlp_health_check():
    """Health check for NLP services"""
    status = {
        "status": "healthy" if BERT_AVAILABLE else "degraded",
        "bert_available": BERT_AVAILABLE,
        "services": {
            "priority_classification": BERT_AVAILABLE,
            "conflict_detection": BERT_AVAILABLE,
            "text_analysis": BERT_AVAILABLE
        }
    }
    
    if not BERT_AVAILABLE:
        status["error"] = "BERT components not available - using fallback systems"
        status["fallback_active"] = True
    else:
        try:
            classifier = get_bert_classifier()
            status["model_trained"] = classifier.is_trained
            status["device"] = str(classifier.device)
        except Exception as e:
            status["initialization_error"] = str(e)
    
    return status