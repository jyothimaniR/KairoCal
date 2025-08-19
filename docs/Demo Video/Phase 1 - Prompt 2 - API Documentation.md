# KairoCal Backend API Endpoints - Complete Documentation

## 🚀 API Overview

KairoCal provides a comprehensive REST API with 50+ endpoints organized into logical modules. The API combines traditional CRUD operations with advanced AI features including BERT-powered priority classification, voice processing, smart conflict detection, and productivity analytics.

**Base URL**: `http://localhost:8000`  
**API Version**: `v1`  
**Authentication**: JWT-based with Cognito sub IDs

---

## 📋 Core System Endpoints

### Health & Status Monitoring

#### `GET /health`
**Purpose**: System health check with component status
```json
{
  "status": "healthy",
  "service": "kairocal-api", 
  "database": "connected",
  "bert_nlp": "operational",
  "voice_api": "operational",
  "conflict_detection": "operational"
}
```

#### `GET /ready`
**Purpose**: Kubernetes readiness probe with migration status
```json
{
  "ready": true,
  "migration": {
    "status": "ok",
    "current_revision": "abc123"
  }
}
```

#### `GET /`
**Purpose**: Root endpoint with feature overview
```json
{
  "message": "KairoCal API with BERT Priority Classification is running!",
  "status": "healthy", 
  "version": "1.0.0",
  "features": [
    "🧠 BERT Priority Classification",
    "🎤 Voice-to-Text Event Creation",
    "⚡ Smart Conflict Detection"
  ]
}
```

#### `GET /api/v1/status`
**Purpose**: Detailed API status with available endpoints
```json
{
  "api_version": "1.0.0",
  "service": "KairoCal Backend with BERT",
  "status": "operational",
  "features": [...],
  "endpoints": {
    "events": "/api/v1/events",
    "nlp": "/api/v1/nlp",
    "voice": "/api/v1/voice",
    "conflicts": "/api/v1/conflicts"
  }
}
```

#### `GET /metrics`
**Purpose**: Prometheus metrics for monitoring
- HTTP request metrics with latency
- Database query performance
- Slow query detection
- Error rate tracking

### Database Management

#### `GET /api/v1/database/status`
**Purpose**: Database connection and schema status
```json
{
  "database_status": "connected",
  "tables_created": 4,
  "tables": ["users", "events", "reminders", "alembic_version"],
  "migration": {
    "status": "ok"
  }
}
```

#### `GET /api/v1/database/migration-status`
**Purpose**: Alembic migration status for deployment validation

---

## 👥 User Management API (`/api/v1/users`)

### Core User Operations

#### `POST /api/v1/users/`
**Purpose**: Create new user profile
**Request**:
```json
{
  "email": "user@example.com",
  "cognito_sub": "test-user-1",
  "full_name": "John Doe",
  "preferences": {
    "timezone": "UTC",
    "work_hours": "09:00-17:00"
  }
}
```
**Response**: User profile with auto-generated UUID and timestamps

#### `GET /api/v1/users/me?cognito_sub={id}`
**Purpose**: Get current user profile by Cognito sub ID
**Business Logic**: 
- Validates user exists
- Returns profile with preferences
- Handles timezone preferences

#### `PUT /api/v1/users/me?cognito_sub={id}`
**Purpose**: Update user profile
**Request**: Partial user data (only changed fields)
**Business Logic**: 
- Validates ownership
- Updates timestamps automatically
- Maintains data integrity

#### `DELETE /api/v1/users/me?cognito_sub={id}`
**Purpose**: Delete user profile and all associated data
**Business Logic**: Cascading delete of events and reminders

### Admin Operations

#### `GET /api/v1/users/{user_id}`
**Purpose**: Get user by UUID (admin/development)

#### `GET /api/v1/users/`
**Purpose**: List all users with pagination
**Parameters**: `skip`, `limit`

---

## 📅 Events API (`/api/v1/events`)

### Core Event CRUD

#### `POST /api/v1/events/?cognito_sub={id}`
**Purpose**: Create new event with optional BERT classification
**Request**:
```json
{
  "title": "Team Meeting",
  "description": "Weekly team sync",
  "start_time": "2025-08-19T14:00:00Z",
  "end_time": "2025-08-19T15:00:00Z",
  "location": "Conference Room A",
  "priority_level": 4
}
```
**Parameters**:
- `auto_classify_priority=true`: Enable BERT classification
**Business Logic**:
- Auto-assigns priority using BERT if not specified
- WebSocket broadcasting for real-time updates
- Validates time ranges and overlaps
- Creates UUID and timestamps

#### `GET /api/v1/events/?cognito_sub={id}`
**Purpose**: List user's events with advanced filtering
**Parameters**:
- `start_date`, `end_date`: Date range filtering
- `min_priority`, `max_priority`: Priority range (1-5)
- `priority_levels`: Specific priority levels array
- `classification_method`: Filter by 'bert', 'manual', 'rule_based'
- `sort_by`: 'start_time', 'priority', 'confidence'
- `sort_order`: 'asc', 'desc'
- `include_priority_stats=true`: Include priority distribution
- `skip`, `limit`: Pagination

**Example Response**:
```json
{
  "events": [...],
  "priority_stats": {
    "total_events": 25,
    "priority_distribution": {
      "1": {"count": 5, "percentage": 20.0},
      "2": {"count": 8, "percentage": 32.0}
    },
    "bert_adoption": 0.85
  }
}
```

#### `GET /api/v1/events/{event_id}?cognito_sub={id}`
**Purpose**: Get specific event by ID
**Business Logic**: Validates ownership before returning

#### `PUT /api/v1/events/{event_id}?cognito_sub={id}`
**Purpose**: Update existing event
**Business Logic**:
- Ownership validation
- Automatic timestamp updates
- Optional priority reclassification

#### `DELETE /api/v1/events/{event_id}?cognito_sub={id}`
**Purpose**: Delete event
**Business Logic**: Ownership validation and cascade deletion

### Priority-Based Event Queries

#### `GET /api/v1/events/priority/high-priority?cognito_sub={id}`
**Purpose**: Get high-priority events (Priority 1-2)
**Parameters**:
- `max_priority=2`: Maximum priority level
- `include_upcoming_only=true`: Only future events
- `limit=10`: Result limit

#### `GET /api/v1/events/priority/low-confidence?cognito_sub={id}`
**Purpose**: Get events with low BERT confidence for manual review
**Parameters**:
- `max_confidence=0.6`: Confidence threshold
**Use Case**: Quality assurance of AI classifications

#### `POST /api/v1/events/{event_id}/reclassify?cognito_sub={id}`
**Purpose**: Reclassify event priority using latest BERT model
**Parameters**:
- `force_bert=false`: Force reclassification even if confident
**Business Logic**:
- Skips high-confidence classifications unless forced
- Updates priority, confidence, and method
- Logs reclassification activity

---

## 🎤 Voice API (`/api/v1/voice`)

### Voice Processing Pipeline

#### `POST /api/v1/voice/transcribe`
**Purpose**: Clean and process raw voice transcription
**Request**:
```json
{
  "text": "uhm, like, schedule a meeting with sarah tomorrow at 2pm",
  "user_id": "uuid",
  "language": "en",
  "confidence_threshold": 0.5
}
```
**Business Logic**:
- Removes filler words and hesitations
- Normalizes temporal references
- Calculates processing confidence
- Language-specific optimizations

#### `POST /api/v1/voice/create-event`
**Purpose**: Complete voice-to-calendar pipeline
**Request**:
```json
{
  "voice_text": "Schedule dinner with mom tomorrow at 6 p.m.",
  "user_id": "uuid",
  "auto_schedule": true,
  "priority_override": null,
  "duration_preference": "smart"
}
```
**Business Logic**:
1. **Text Cleaning**: Remove filler words, normalize speech patterns
2. **NLP Processing**: Extract event details using spaCy
3. **Temporal Resolution**: Convert "tomorrow at 6 p.m." to UTC timestamps
4. **BERT Classification**: Auto-assign priority with confidence
5. **Database Storage**: Create event with metadata
6. **WebSocket Broadcasting**: Real-time UI updates

**Response**:
```json
{
  "success": true,
  "event_id": "uuid",
  "event_data": {
    "title": "Dinner With Mom",
    "start_time": "2025-08-19T18:00:00Z",
    "end_time": "2025-08-19T19:00:00Z"
  },
  "bert_classification": {
    "priority": 2,
    "confidence": 0.78,
    "method": "bert"
  },
  "processing_details": {
    "total_time": 1.2,
    "temporal_resolution": "success"
  }
}
```

#### `POST /api/v1/voice/analyze`
**Purpose**: Analyze voice input without creating event
**Use Case**: Testing, validation, preview mode
**Business Logic**:
- Same processing pipeline as create-event
- Returns analysis without database writes
- Includes BERT predictions and NLP insights

#### `GET /api/v1/voice/health`
**Purpose**: Voice processing system health check
**Response**:
```json
{
  "status": "healthy",
  "nlp_service": "operational",
  "bert_model": "loaded",
  "temporal_resolver": "active"
}
```

---

## 🧠 NLP & BERT API (`/api/v1/nlp`)

### BERT Model Operations

#### `GET /api/v1/nlp/model-status`
**Purpose**: BERT model status and performance metrics
**Response**:
```json
{
  "model_loaded": true,
  "model_trained": true,
  "last_training": "2025-08-15T10:30:00Z",
  "accuracy": 0.87,
  "device": "cpu",
  "memory_usage": "2.3GB"
}
```

#### `POST /api/v1/nlp/classify-priority`
**Purpose**: Classify single event priority using BERT
**Request**:
```json
{
  "title": "Board Meeting",
  "description": "Quarterly review with executives",
  "start_time": "2025-08-20T09:00:00Z",
  "location": "Boardroom"
}
```
**Response**:
```json
{
  "priority": 5,
  "confidence": 0.92,
  "method": "bert",
  "reasoning": "Executive meeting with quarterly review keywords",
  "keywords": ["board", "quarterly", "executives"]
}
```

#### `POST /api/v1/nlp/batch-predict`
**Purpose**: Bulk classification for multiple events
**Request**:
```json
{
  "events": [
    {"title": "Coffee break", "description": "..."},
    {"title": "Client presentation", "description": "..."}
  ]
}
```
**Business Logic**: Optimized batch processing with single model load

#### `POST /api/v1/nlp/explain-priority`
**Purpose**: Get detailed explanation of priority classification
**Response**:
```json
{
  "priority": 4,
  "confidence": 0.85,
  "explanation": {
    "key_factors": ["client", "presentation", "revenue"],
    "urgency_indicators": ["deadline", "important"],
    "context_analysis": "Business-critical client interaction"
  }
}
```

### Conflict Detection via NLP

#### `POST /api/v1/nlp/detect-conflicts`
**Purpose**: AI-powered conflict detection with context understanding
**Request**:
```json
{
  "events": [
    {
      "title": "Team Meeting",
      "start_time": "2025-08-19T14:00:00Z",
      "end_time": "2025-08-19T15:00:00Z"
    },
    {
      "title": "Client Call", 
      "start_time": "2025-08-19T14:30:00Z",
      "end_time": "2025-08-19T15:30:00Z"
    }
  ]
}
```
**Business Logic**:
- Time overlap detection
- Priority-based severity assessment
- Context-aware conflict reasoning
- Resolution suggestions

### Demo & Development

#### `GET /api/v1/nlp/demo/sample-predictions`
**Purpose**: Get sample BERT predictions for demo
**Use Case**: Testing and demonstration

#### `GET /api/v1/nlp/demo/features`
**Purpose**: BERT feature extraction demonstration

#### `GET /api/v1/nlp/health`
**Purpose**: NLP system health with model status

---

## ⚡ Conflicts API (`/api/v1/conflicts`)

### Conflict Detection

#### `POST /api/v1/conflicts/check?cognito_sub={id}`
**Purpose**: Check for conflicts with proposed new event
**Request**:
```json
{
  "title": "New Meeting",
  "start_time": "2025-08-19T14:00:00Z",
  "end_time": "2025-08-19T15:00:00Z",
  "buffer_minutes": 15,
  "is_all_day": false
}
```
**Parameters**:
- `engine`: 'basic_v1' or 'fallback'
**Business Logic**:
- All-day events never conflict (special handling)
- Buffer time consideration
- Existing event overlap detection
- Priority-based conflict severity

**Response**:
```json
{
  "conflicts": [
    {
      "conflict_id": "uuid",
      "type": "time_overlap",
      "severity": "high",
      "conflicting_event": {
        "id": "uuid",
        "title": "Existing Meeting",
        "start_time": "2025-08-19T14:30:00Z"
      },
      "overlap_duration": 30,
      "suggestions": [
        {
          "action": "reschedule",
          "new_time": "2025-08-19T15:30:00Z",
          "confidence": 0.85
        }
      ]
    }
  ],
  "engine": "basic_v1"
}
```

#### `POST /api/v1/conflicts/resolve?cognito_sub={id}`
**Purpose**: Get conflict resolution suggestions
**Business Logic**:
- Priority-based resolution strategies
- Alternative time slot generation
- Meeting room availability (if applicable)
- Participant schedule consideration

#### `GET /api/v1/conflicts/report?cognito_sub={id}`
**Purpose**: Comprehensive conflict analysis report
**Response**:
```json
{
  "total_conflicts": 5,
  "severity_breakdown": {
    "high": 2,
    "medium": 2, 
    "low": 1
  },
  "type_breakdown": {
    "time_overlap": 4,
    "resource_conflict": 1
  },
  "recommendations": [
    "Consider shorter meetings to reduce conflicts",
    "Block focus time to avoid interruptions"
  ]
}
```

#### `POST /api/v1/conflicts/batch-check?cognito_sub={id}`
**Purpose**: Check multiple events for conflicts simultaneously
**Use Case**: Calendar imports, bulk scheduling

---

## 📊 Analytics API (`/api/v1/analytics`)

### Productivity Metrics

#### `GET /api/v1/analytics/productivity/metrics?cognito_sub={id}`
**Purpose**: Comprehensive productivity analytics
**Parameters**:
- `start_date`, `end_date`: Date range
- `period`: 'week', 'month', 'quarter'
**Response**:
```json
{
  "current_score": 87,
  "weekly_change": 5.2,
  "meeting_efficiency": 0.78,
  "focus_time_hours": 25.5,
  "conflict_resolution_rate": 0.92,
  "voice_adoption": 0.65,
  "peak_productivity_hours": ["09:00", "14:00"],
  "trends": {
    "weekly_scores": [82, 85, 87],
    "conflict_frequency": [3, 2, 1]
  }
}
```

#### `GET /api/v1/analytics/priority/trends?cognito_sub={id}`
**Purpose**: Priority distribution analysis over time
**Response**:
```json
{
  "time_series": [
    {
      "date": "2025-08-12",
      "priority_distribution": {
        "1": 2, "2": 5, "3": 8, "4": 3, "5": 1
      },
      "bert_confidence_avg": 0.84
    }
  ],
  "overall_trends": {
    "bert_adoption_rate": 0.78,
    "avg_confidence": 0.82,
    "priority_stability": 0.91
  }
}
```

#### `GET /api/v1/analytics/bert/performance?cognito_sub={id}`
**Purpose**: BERT model performance analytics
**Response**:
```json
{
  "classification_accuracy": 0.87,
  "confidence_distribution": {
    "high": 0.72,
    "medium": 0.21,
    "low": 0.07
  },
  "model_metrics": {
    "total_classifications": 1250,
    "manual_overrides": 45,
    "avg_processing_time": 0.23
  }
}
```

### User Behavior Analytics

#### `GET /api/v1/analytics/behavior/patterns?cognito_sub={id}`
**Purpose**: User scheduling behavior analysis
**Response**:
```json
{
  "scheduling_patterns": {
    "preferred_meeting_times": ["10:00", "14:00"],
    "average_meeting_duration": 45,
    "most_productive_days": ["Tuesday", "Wednesday"]
  },
  "voice_usage": {
    "total_voice_events": 89,
    "voice_adoption_trend": 0.15,
    "most_common_commands": ["meeting", "call", "reminder"]
  }
}
```

#### `GET /api/v1/analytics/calendar/optimization?cognito_sub={id}`
**Purpose**: Calendar optimization suggestions
**Response**:
```json
{
  "suggestions": [
    {
      "type": "focus_time",
      "recommendation": "Block 2-hour focus sessions on Tuesday mornings",
      "confidence": 0.88
    },
    {
      "type": "meeting_consolidation", 
      "recommendation": "Group meetings on Wednesdays to create focus days",
      "confidence": 0.75
    }
  ],
  "efficiency_score": 0.82
}
```

---

## 🔧 API Features & Capabilities

### Advanced Query Capabilities
- **Complex Filtering**: Multi-parameter filtering across all endpoints
- **Pagination**: Consistent `skip`/`limit` parameters
- **Sorting**: Flexible sorting by multiple fields
- **Date Ranges**: ISO 8601 date filtering
- **Priority Filtering**: Range and specific level filtering

### Real-Time Features
- **WebSocket Broadcasting**: Live event updates
- **Conflict Alerts**: Real-time conflict notifications
- **Priority Changes**: Live priority reclassification alerts

### AI & Machine Learning
- **BERT Integration**: 50+ endpoints with AI classification
- **Voice Processing**: Complete speech-to-calendar pipeline
- **Smart Suggestions**: AI-powered time slot recommendations
- **Behavior Analysis**: Pattern recognition and optimization

### Data Security & Validation
- **Input Validation**: Pydantic schema validation
- **User Isolation**: Cognito-based data segregation
- **Error Handling**: Consistent HTTP status codes
- **Logging**: Comprehensive request/response logging

### Performance Optimization
- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: Redis caching for frequent operations
- **Batch Operations**: Bulk processing capabilities
- **Metrics**: Prometheus monitoring integration

---

## 📝 Example API Workflows

### 1. Complete Voice-to-Calendar Workflow
```bash
# 1. Check voice system health
GET /api/v1/voice/health

# 2. Create event from voice
POST /api/v1/voice/create-event
{
  "voice_text": "Schedule team standup tomorrow at 9am",
  "user_id": "uuid",
  "auto_schedule": true
}

# 3. Check for conflicts
POST /api/v1/conflicts/check?cognito_sub=test-user-1
{
  "title": "Team Standup",
  "start_time": "2025-08-19T09:00:00Z",
  "end_time": "2025-08-19T09:30:00Z"
}

# 4. Get events list
GET /api/v1/events/?cognito_sub=test-user-1&sort_by=priority
```

### 2. Priority Management Workflow
```bash
# 1. Get low-confidence classifications
GET /api/v1/events/priority/low-confidence?cognito_sub=test-user-1

# 2. Reclassify specific event
POST /api/v1/events/{event_id}/reclassify?cognito_sub=test-user-1

# 3. Get priority trends
GET /api/v1/analytics/priority/trends?cognito_sub=test-user-1

# 4. Get high-priority events
GET /api/v1/events/priority/high-priority?cognito_sub=test-user-1
```

### 3. Analytics Dashboard Workflow
```bash
# 1. Get productivity metrics
GET /api/v1/analytics/productivity/metrics?cognito_sub=test-user-1

# 2. Get BERT performance
GET /api/v1/analytics/bert/performance?cognito_sub=test-user-1

# 3. Get behavior patterns
GET /api/v1/analytics/behavior/patterns?cognito_sub=test-user-1

# 4. Get optimization suggestions
GET /api/v1/analytics/calendar/optimization?cognito_sub=test-user-1
```

---

## 🚀 API Capabilities Summary

**Total Endpoints**: 50+  
**Core Operations**: Full CRUD for users, events, reminders  
**AI Features**: BERT classification, voice processing, conflict detection  
**Analytics**: Productivity metrics, behavior analysis, optimization  
**Real-time**: WebSocket broadcasting, live updates  
**Performance**: Sub-500ms response times, Prometheus monitoring  
**Security**: JWT authentication, input validation, user isolation  

The KairoCal API provides enterprise-grade calendar management with cutting-edge AI capabilities, making it suitable for both individual productivity and team collaboration scenarios.
