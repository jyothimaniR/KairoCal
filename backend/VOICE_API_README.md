# Voice-to-Text API for KairoCal

## Overview

The Voice-to-Text API provides comprehensive voice command processing for KairoCal, enabling users to create calendar events through natural language voice input. The system integrates seamlessly with the existing BERT priority classification system for intelligent event management.

## Features

### 🎤 Voice Processing
- **Voice Text Cleaning**: Removes filler words (um, uh, like, etc.)
- **Pattern Recognition**: Identifies voice-specific patterns and corrections
- **Confidence Scoring**: Provides reliability assessment for voice commands
- **Multi-language Support**: Extensible language processing framework

### 🧠 NLP Integration
- **Entity Extraction**: Automatically detects titles, times, locations, participants
- **Temporal Processing**: Handles relative time references (tomorrow, next week)
- **Priority Detection**: Identifies urgency keywords and context
- **Event Type Classification**: Categorizes meetings, appointments, calls, etc.

### 🤖 BERT Integration
- **Smart Priority Classification**: Uses trained BERT model for accurate priority assessment
- **Fallback System**: Rule-based priority classification when BERT unavailable
- **Confidence Metrics**: Provides prediction confidence scores
- **Full Pipeline**: Voice → NLP → BERT → Database

## API Endpoints

### 1. Voice Transcription
```bash
POST /api/v1/voice/transcribe
```
Process and clean voice input text.

**Request:**
```json
{
  "text": "Um, schedule a meeting with John tomorrow at 3pm",
  "user_id": 1,
  "language": "en",
  "confidence_threshold": 0.5
}
```

**Response:**
```json
{
  "transcribed_text": "Um, schedule a meeting with John tomorrow at 3pm",
  "cleaned_text": "schedule meeting with john tomorrow at 3pm",
  "confidence": 0.85,
  "processing_time": 0.123,
  "timestamp": "2025-08-01T21:30:00",
  "metadata": {
    "original_word_count": 10,
    "cleaned_word_count": 8,
    "words_removed": 2
  }
}
```

### 2. Voice Event Creation
```bash
POST /api/v1/voice/create-event
```
Create calendar event from voice input with full BERT integration.

**Request:**
```json
{
  "voice_text": "URGENT: Client presentation deadline tomorrow at 2pm in conference room A",
  "user_id": 1,
  "auto_schedule": true,
  "priority_override": null
}
```

**Response:**
```json
{
  "success": true,
  "event_id": 123,
  "event_data": {
    "title": "Client Presentation Deadline",
    "start_time": "2025-08-02T14:00:00",
    "location": "Conference Room A",
    "priority": 4
  },
  "nlp_analysis": {
    "cleaned_text": "urgent client presentation deadline tomorrow at 2pm in conference room a",
    "extracted_title": "Client Presentation Deadline",
    "extracted_time": "2025-08-02T14:00:00",
    "extracted_location": "Conference Room A"
  },
  "bert_classification": {
    "priority": 4,
    "confidence": 0.876,
    "model_used": "BERT",
    "final_priority": 4
  },
  "processing_details": {
    "total_processing_time": 1.234,
    "words_removed": 1
  },
  "message": "✅ Event created successfully from voice input with priority 4"
}
```

### 3. Voice Analysis
```bash
POST /api/v1/voice/analyze-voice
```
Analyze voice input without creating an event (useful for testing).

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/voice/analyze-voice" \
  -d "voice_text=Schedule urgent meeting tomorrow&user_id=1"
```

### 4. Health Check
```bash
GET /api/v1/voice/health
```
Check voice API status and component availability.

## Usage Examples

### cURL Commands

#### 1. Create Urgent Meeting
```bash
curl -X POST "http://localhost:8000/api/v1/voice/create-event" \
  -H "Content-Type: application/json" \
  -d '{
    "voice_text": "URGENT: Emergency board meeting now in main conference room",
    "user_id": 1,
    "auto_schedule": true
  }' | jq '.'
```

#### 2. Schedule Doctor Appointment
```bash
curl -X POST "http://localhost:8000/api/v1/voice/create-event" \
  -H "Content-Type: application/json" \
  -d '{
    "voice_text": "Book doctor appointment next Tuesday at 2:30pm",
    "user_id": 1,
    "auto_schedule": true
  }' | jq '.'
```

#### 3. Casual Team Event
```bash
curl -X POST "http://localhost:8000/api/v1/voice/create-event" \
  -H "Content-Type: application/json" \
  -d '{
    "voice_text": "Coffee break with team next Friday afternoon",
    "user_id": 1,
    "auto_schedule": true
  }' | jq '.'
```

### Python Examples

#### Basic Voice Processing
```python
import requests

# Create event from voice
response = requests.post(
    "http://localhost:8000/api/v1/voice/create-event",
    json={
        "voice_text": "Schedule important client meeting tomorrow at 3pm",
        "user_id": 1,
        "auto_schedule": True
    }
)

result = response.json()
print(f"Event created: {result['success']}")
print(f"Priority: {result['bert_classification']['final_priority']}")
print(f"Confidence: {result['bert_classification']['confidence']:.3f}")
```

#### Voice Text Cleaning
```python
response = requests.post(
    "http://localhost:8000/api/v1/voice/transcribe",
    json={
        "text": "Um, like, schedule a meeting with, uh, John tomorrow",
        "user_id": 1
    }
)

result = response.json()
print(f"Original: {result['transcribed_text']}")
print(f"Cleaned: {result['cleaned_text']}")
```

## Testing

### 1. Implementation Test
```bash
python test_voice_implementation.py
```
Validates that all components are working correctly.

### 2. API Testing Suite
```bash
python test_voice_api.py
```
Comprehensive testing of all voice API endpoints.

### 3. Demo Script
```bash
# Quick demo with one example per priority level
python demo_voice_commands.py --quick-demo

# Full demo with all examples
python demo_voice_commands.py

# Generate cURL examples
python demo_voice_commands.py --curl-examples
```

## Integration with Existing Systems

### BERT Priority Classification
- Seamlessly integrates with existing BERT model
- Falls back to rule-based classification if BERT unavailable
- Provides confidence scores for all predictions

### Database Integration
- Uses existing Event and User models
- Maintains all existing relationships and constraints
- Supports full event lifecycle management

### NLP Pipeline
- Extends existing NLP service with voice-specific processing
- Maintains compatibility with text-based input
- Enhanced entity extraction for voice patterns

## Voice Command Examples

### Critical Priority (5)
- "URGENT: Emergency board meeting now"
- "ASAP: Production server down need meeting immediately"
- "CRITICAL: CEO wants quarterly results right away"

### High Priority (4)
- "Important client presentation tomorrow at 2pm"
- "Deadline: Submit project proposal by end of day"
- "High priority interview with candidate next Tuesday"

### Medium Priority (3)
- "Weekly team standup meeting next Monday at 9am"
- "Doctor appointment for annual checkup next Thursday"
- "Monthly project review with stakeholders"

### Low Priority (2)
- "Optional workshop on productivity techniques"
- "Casual team lunch at new restaurant"
- "Training session on optional tools"

### Very Low Priority (1)
- "Informal coffee break with colleagues"
- "Social happy hour event next Friday"
- "Casual walk and talk meeting"

## Configuration

### Environment Variables
```bash
# API Configuration
VOICE_API_ENABLED=true
VOICE_CONFIDENCE_THRESHOLD=0.5
VOICE_AUTO_SCHEDULE=true

# BERT Integration
BERT_MODEL_PATH=models/bert_priority_classifier
BERT_FALLBACK_ENABLED=true

# NLP Service
NLP_VOICE_PROCESSING=true
NLP_FILLER_WORD_REMOVAL=true
```

### Voice Processor Settings
```python
# Filler words (customizable)
voice_fillers = [
    'um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'well'
]

# Confidence thresholds
confidence_thresholds = {
    'transcription': 0.8,
    'nlp_analysis': 0.7,
    'event_creation': 0.6
}
```

## Error Handling

### Common Error Responses
```json
{
  "detail": "Voice transcription failed: Invalid input text",
  "status_code": 400
}
```

### Fallback Behavior
- BERT unavailable → Rule-based priority classification
- Voice processing error → Text-based NLP processing
- Entity extraction failure → Manual field completion

## Performance

### Typical Response Times
- Voice transcription: 50-150ms
- NLP analysis: 100-300ms
- BERT classification: 200-500ms
- Event creation: 300-800ms
- **Total pipeline: 650-1750ms**

### Optimization Tips
- Use `analyze-voice` endpoint for testing without database writes
- Batch process multiple voice commands when possible
- Cache BERT model for faster repeated predictions

## Development

### Adding New Voice Patterns
```python
# Add to voice_patterns in VoiceProcessor
voice_patterns = {
    r'\bremind me to\b': 'reminder:',
    r'\bschedule\s+(a\s+)?meeting\b': 'meeting',
    # Add your patterns here
}
```

### Extending NLP Processing
```python
# Override process_voice_input in NLPService
async def process_voice_input(self, voice_text: str) -> Dict[str, Any]:
    # Your custom processing logic
    pass
```

### Custom Priority Rules
```python
# Extend priority_indicators in VoiceProcessor
priority_indicators = {
    5: ['urgent', 'emergency', 'critical'],
    # Add your priority keywords
}
```

## Security Considerations

- All voice input is processed server-side
- No voice audio files are stored
- User authentication required for all endpoints
- Input validation and sanitization applied
- Rate limiting recommended for production use

## Support

For issues, questions, or feature requests related to the Voice API:

1. Check the test suite results: `python test_voice_implementation.py`
2. Review API health status: `GET /api/v1/voice/health`
3. Run demos to validate functionality: `python demo_voice_commands.py`
4. Check BERT model status: `GET /api/v1/nlp/model-status`

The Voice-to-Text API is designed to seamlessly extend KairoCal's existing capabilities while maintaining full compatibility with the BERT priority classification system.
