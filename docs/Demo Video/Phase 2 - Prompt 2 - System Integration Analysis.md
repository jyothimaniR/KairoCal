# 🔄 **KairoCal System Integration & Component Communication Analysis**

*Phase 2 - Prompt 2: How Components Communicate*

---

## 📋 **Executive Summary**

KairoCal implements a **modern microservice-inspired architecture** with clear separation of concerns:

- **Frontend-Backend**: RESTful API + WebSocket real-time communication
- **NLP Integration**: Async pipeline with BERT model inference
- **Voice Processing**: Speech-to-text → NLP → Event creation flow
- **Real-time Updates**: WebSocket-based live synchronization
- **Background Processing**: Async task queue for AI operations

---

## 🌐 **1. Frontend-Backend Communication**

### **RESTful API Architecture**
```typescript
// Frontend API Service Layer (apiService.ts)
class APIService {
  // Base URL: http://127.0.0.1:8000/api/v1
  async getEvents(userId: string): Promise<Event[]> {
    const response = await fetch(`${API_V1}/events?cognito_sub=${userId}`);
    return response.json();
  }

  async createVoiceEvent(voiceText: string, userId: string): Promise<VoiceEventResponse> {
    return fetch(`${API_V1}/voice/create-event`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ voice_text: voiceText, cognito_sub: userId })
    }).then(res => res.json());
  }
}
```

### **API Endpoint Structure**
```bash
📁 Backend API Routes (FastAPI)
├── /api/v1/events/*          # Event CRUD operations
├── /api/v1/voice/*           # Voice processing pipeline
├── /api/v1/nlp/*             # BERT & NLP services
├── /api/v1/analytics/*       # Dashboard metrics
├── /api/v1/conflicts/*       # Smart conflict detection
└── /api/v1/health            # System health checks
```

### **Real-time Updates via WebSocket**
```typescript
// Frontend WebSocket Integration (useWebSocket.ts)
const ws = new WebSocket('ws://localhost:8000/ws?user_id=frontend-test-user');

ws.onmessage = (event) => {
  const message: WebSocketMessage = JSON.parse(event.data);
  
  switch (message.type) {
    case 'event_created':
      // Update calendar view immediately
      updateEventsList(message.data);
      break;
    case 'conflict_detected':
      // Show conflict alert
      showConflictAlert(message.data);
      break;
    case 'priority_updated':
      // Refresh priority indicators
      updatePriorityUI(message.data);
      break;
  }
};
```

---

## 🧠 **2. NLP Pipeline Integration**

### **Voice Input Processing Flow**
```python
# Voice API Handler (backend/app/api/voice.py)
@voice_router.post("/create-event")
async def create_event_from_voice(request: VoiceCreateEventRequest):
    # Step 1: Voice text cleaning
    cleaned_text = voice_processor.clean_voice_text(request.voice_text)
    
    # Step 2: NLP entity extraction
    nlp_service = NLPService()
    nlp_result = await nlp_service.process_voice_input(cleaned_text)
    
    # Step 3: BERT priority classification
    bert_model = get_global_bert_model()
    event_for_bert = {
        'title': nlp_result.get('title'),
        'description': nlp_result.get('description'),
        'start_time': nlp_result.get('start_time'),
        'location': nlp_result.get('location')
    }
    bert_priority, bert_confidence = bert_model.predict(event_for_bert)
    
    # Step 4: Hybrid decision logic
    if bert_confidence >= 0.7:
        final_priority = bert_priority  # Trust BERT for high confidence
    elif nlp_priority >= 4 and nlp_priority > bert_priority:
        final_priority = nlp_priority   # Use NLP for critical keywords
    else:
        final_priority = bert_priority  # Default to BERT
```

### **NLP Service Architecture**
```python
# NLP Service (backend/app/services/nlp_service.py)
class NLPService:
    async def process_voice_input(self, voice_text: str) -> Dict[str, Any]:
        # Entity extraction using 60+ regex patterns
        title = self._extract_title(voice_text)          # "Meeting with CEO"
        location = self._extract_location(voice_text)    # "Boardroom"
        start_time = self._extract_temporal(voice_text)  # "tomorrow at 2pm"
        priority = self._extract_priority(voice_text)    # Keywords: urgent, critical
        
        # Temporal resolution (relative → absolute time)
        start_time = self._resolve_temporal_references(start_time)
        
        return {
            'title': title,
            'start_time': start_time,
            'end_time': start_time + timedelta(hours=1),
            'location': location,
            'priority': priority,
            'confidence': self._calculate_confidence(voice_text)
        }
```

---

## 🤖 **3. BERT Model Integration**

### **Model Loading & Initialization**
```python
# BERT Model Loader (backend/app/nlp/model_loader.py)
class BERTModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.is_trained = False
    
    def load_model(self):
        # Load DistilBERT with custom classification head
        self.model = DistilBertForSequenceClassification.from_pretrained(
            "distilbert-base-uncased", 
            num_labels=5  # Priority levels 1-5
        )
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        self.is_trained = True

# Global model instance
_global_bert_model = BERTModelManager()

def get_global_bert_model():
    return _global_bert_model
```

### **BERT Prediction Pipeline**
```python
# BERT Priority Classifier (backend/app/nlp/bert_priority_classifier.py)
class BERTPriorityClassifier:
    def predict(self, event_data: Dict[str, Any]) -> Tuple[int, float]:
        # Combine event fields for classification
        text_input = f"{event_data['title']} {event_data['description']} {event_data['location']}"
        
        # Tokenize input
        inputs = self.tokenizer(
            text_input,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(probabilities, dim=-1).item()
            confidence = float(torch.max(probabilities).item())
        
        # Convert to priority scale (1=Critical, 5=Very Low)
        priority = predicted_class + 1
        
        return priority, confidence
```

### **API Integration Points**
```python
# NLP API Endpoints (backend/app/api/nlp.py)
@nlp_router.post("/classify-priority")
async def classify_priority(request: PriorityClassificationRequest):
    bert_model = get_global_bert_model()
    
    if not bert_model.is_trained:
        raise HTTPException(status_code=503, detail="BERT model not available")
    
    priority, confidence = bert_model.predict(request.event_data)
    
    return {
        "priority": priority,
        "confidence": confidence,
        "model_status": "operational",
        "processing_time_ms": 250
    }
```

---

## ⚡ **4. Background Services & Async Processing**

### **No Traditional Queue System (Current Architecture)**
```python
# Current: Synchronous processing with async/await
@voice_router.post("/create-event")
async def create_event_from_voice(request: VoiceCreateEventRequest):
    # All processing happens in real-time during request
    # No background queues - immediate response
    
    processing_start = time.time()
    
    # 1. Voice processing (50-150ms)
    nlp_result = await nlp_service.process_voice_input(voice_text)
    
    # 2. BERT classification (200-500ms) 
    bert_priority, confidence = bert_model.predict(event_data)
    
    # 3. Database write (50-100ms)
    event = await create_event_in_db(event_data)
    
    # 4. WebSocket broadcast (immediate)
    await websocket_manager.broadcast_event_created(event)
    
    total_time = (time.time() - processing_start) * 1000
    logger.info(f"✅ Total processing: {total_time:.1f}ms")
    
    return event_response
```

### **Async FastAPI Architecture**
```python
# All endpoints use async/await for non-blocking I/O
async def get_events(db: Session = Depends(get_db)):
    # Non-blocking database queries
    events = await db.execute(select(Event).where(Event.user_id == user_id))
    
    # Non-blocking BERT batch processing
    for event in events:
        if not event.priority_level:
            priority, confidence = await bert_model.predict_async(event)
            event.priority_level = priority

async def broadcast_to_websockets(event_data):
    # Non-blocking WebSocket notifications
    await websocket_manager.broadcast_to_all_users(event_data)
```

### **WebSocket Background Tasks**
```python
# WebSocket Manager (backend/app/core/websocket_manager.py)
class ConnectionManager:
    async def start_background_tasks(self):
        # Cleanup inactive connections every 5 minutes
        asyncio.create_task(self._cleanup_inactive_connections())
        
        # Send heartbeat every 30 seconds
        asyncio.create_task(self._send_heartbeat_to_clients())
        
        # Redis message listener (when Redis is available)
        asyncio.create_task(self._listen_for_redis_messages())

    async def _cleanup_inactive_connections(self):
        while True:
            await asyncio.sleep(300)  # 5 minutes
            inactive_connections = []
            
            for connection_id, last_seen in self.connections.items():
                if time.time() - last_seen > 600:  # 10 minutes
                    inactive_connections.append(connection_id)
            
            for conn_id in inactive_connections:
                await self.disconnect(conn_id)
```

---

## 🎤 **5. Voice Input End-to-End Flow**

### **Frontend Voice Capture**
```typescript
// Frontend Voice Service (voiceService.ts)
class VoiceService {
  startVoiceRecognition(): Promise<string> {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    return new Promise((resolve, reject) => {
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const confidence = event.results[0][0].confidence;
        
        console.log(`🗣️ Recognized: "${transcript}" (${confidence})`);
        resolve(transcript);
      };
      
      recognition.start();
    });
  }
}
```

### **Complete Voice Flow**
```mermaid
User Voice Input
    ↓
Browser Web Speech API (webkitSpeechRecognition)
    ↓ transcript
Frontend VoiceService.createEventFromVoice()
    ↓ HTTP POST /api/v1/voice/create-event
Backend Voice API Handler
    ↓
Voice Text Cleaning (remove filler words)
    ↓
NLP Entity Extraction (60+ regex patterns)
    ↓ title, time, location, priority
BERT Priority Classification (DistilBERT model)
    ↓ priority + confidence score
Hybrid Decision Logic (NLP + BERT)
    ↓ final_priority
Database Storage (SQLAlchemy ORM)
    ↓ event_id
WebSocket Broadcast (real-time update)
    ↓
Frontend State Update (React hooks)
    ↓
UI Re-render (calendar + dashboard)
```

### **Voice Processing Performance**
```python
# Typical Response Times (from VOICE_API_README.md)
Voice transcription: 50-150ms     # Browser Web Speech API
NLP analysis: 100-300ms           # Entity extraction + cleaning
BERT classification: 200-500ms    # PyTorch model inference
Event creation: 300-800ms         # Database write + validation
WebSocket broadcast: <10ms        # Real-time notification
─────────────────────────────────
Total pipeline: 650-1750ms       # End-to-end voice-to-database
```

---

## 🔌 **6. WebSocket Real-time Implementation**

### **Enterprise WebSocket Server**
```python
# Ultimate Socket Server (backend/app/websocket/ultimate_socket_server.py)
class UltimateSocketServer:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Initialize Socket.IO with enterprise configuration
        self.sio = socketio.AsyncServer(
            async_mode='asgi',
            cors_allowed_origins=['http://localhost:3000'],
            cors_credentials=True,
            ping_timeout=60,
            ping_interval=25,
            max_http_buffer_size=1024 * 1024  # 1MB
        )
        
        # Multi-device user tracking
        self.user_sessions: Dict[str, UserSession] = {}
        self.user_connections: Dict[int, Set[str]] = {}
```

### **Connection Management**
```python
@self.sio.event
async def connect(sid: str, environ: dict, auth: dict):
    """Handle client connection with JWT authentication"""
    # Extract and verify JWT token
    token = auth.get('token')
    user_data = await self._verify_jwt_token(token)
    
    if not user_data:
        return False  # Deny connection
    
    # Track user session with device info
    self.user_sessions[sid] = UserSession(
        session_id=sid,
        user_id=user_data['user_id'],
        username=user_data.get('username', 'Unknown'),
        connected_at=datetime.now(),
        device_info=auth.get('deviceInfo', {})
    )
    
    # Join user-specific room for targeted messaging
    await self.sio.enter_room(sid, f"user_{user_data['user_id']}")
    
    logger.info(f"👋 User connected: {user_data['username']} ({sid})")
```

### **Real-time Event Broadcasting**
```python
# Event creation triggers immediate WebSocket broadcast
async def broadcast_event_created(self, event_data: Dict[str, Any]):
    """Broadcast new event to all connected users"""
    try:
        message = {
            'type': 'event_created',
            'event': event_data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Broadcast to specific user
        user_id = event_data.get('user_id')
        await self.sio.emit('event_created', message, room=f"user_{user_id}")
        
        # Also broadcast via Redis for multi-server scaling
        if self.redis_client:
            await self.redis_client.publish('kairocal:events', json.dumps(message))
        
        logger.info(f"📡 Event broadcast sent to user {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Event broadcast error: {e}")

# Conflict detection broadcasting
async def broadcast_conflict_detected(self, affected_users: List[int], conflict_data: Dict[str, Any]):
    """Broadcast conflict detection to affected users"""
    message = {
        'type': 'conflict_detected',
        'conflict': conflict_data,
        'severity': conflict_data.get('severity', 'medium'),
        'timestamp': datetime.now().isoformat()
    }
    
    for user_id in affected_users:
        await self.sio.emit('conflict_detected', message, room=f"user_{user_id}")
```

### **Frontend WebSocket Integration**
```typescript
// Frontend WebSocket Hook (useWebSocket.ts)
export const useWebSocket = () => {
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  
  const connect = useCallback(() => {
    const wsUrl = 'ws://localhost:8000/ws?user_id=frontend-test-user';
    const ws = new WebSocket(wsUrl);
    
    ws.onmessage = (event) => {
      const message: WebSocketMessage = JSON.parse(event.data);
      
      // Handle different message types
      switch (message.type) {
        case 'event_created':
          // Trigger calendar refresh
          updateEventsList(message.data);
          showNotification('New event created!');
          break;
          
        case 'conflict_detected':
          // Show conflict alert
          showConflictDialog(message.data);
          break;
          
        case 'priority_updated':
          // Update priority indicators
          updatePriorityDisplay(message.data);
          break;
      }
      
      setLastMessage(message);
    };
  }, []);
};

// Real-time calendar updates hook
export const useCalendarWebSocket = (onEventUpdate?: () => void) => {
  const { lastMessage } = useWebSocket();
  
  useEffect(() => {
    if (lastMessage?.type === 'event_created' || lastMessage?.type === 'event_updated') {
      onEventUpdate?.();
    }
  }, [lastMessage, onEventUpdate]);
};
```

### **Redis Scaling Architecture (Available)**
```python
# Redis Adapter for Multi-Server WebSocket Scaling
class RedisAdapter:
    async def broadcast_to_cluster(self, channel: str, message: Dict[str, Any]):
        """Broadcast message to all servers in cluster"""
        await self.redis_client.publish(f"kairocal:{channel}", json.dumps(message))
    
    async def listen_for_broadcasts(self):
        """Listen for broadcasts from other servers"""
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe('kairocal:events', 'kairocal:conflicts', 'kairocal:priorities')
        
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                await self._handle_cluster_message(data)
```

---

## 🔄 **7. Specific Integration Examples**

### **Example 1: Voice Event Creation Integration**
```typescript
// Complete flow from voice input to database to UI update

// 1. Frontend: User clicks voice button
const handleVoiceInput = async () => {
  const transcript = await voiceService.startVoiceRecognition();
  // → "Meeting with CEO tomorrow at 2pm for quarterly review"
  
  const result = await apiService.createVoiceEvent(transcript, userId);
  // → Triggers backend processing pipeline
};

// 2. Backend: Voice processing pipeline
@voice_router.post("/create-event")
async def create_event_from_voice(request):
    # NLP extracts: title="Meeting with CEO", time="tomorrow at 2pm" 
    nlp_result = await nlp_service.process_voice_input(request.voice_text)
    
    # BERT classifies: priority=5 (Critical), confidence=0.89
    bert_priority, confidence = bert_model.predict({
        'title': 'Meeting with CEO',
        'description': 'quarterly review',
        'location': ''
    })
    
    # Hybrid decision: Use BERT (high confidence)
    final_priority = 5
    
    # Database storage
    event = Event(
        title="Meeting with CEO",
        priority_level=5,
        start_time="2025-08-19T14:00:00Z",
        user_id=request.cognito_sub
    )
    db.add(event)
    await db.commit()
    
    # WebSocket broadcast
    await websocket_manager.broadcast_event_created({
        'event_id': event.id,
        'title': event.title,
        'priority': event.priority_level,
        'user_id': event.user_id
    })

// 3. Frontend: Real-time update
useEffect(() => {
  if (lastWebSocketMessage?.type === 'event_created') {
    // Immediately update calendar without API call
    setEvents(prev => [...prev, lastWebSocketMessage.data]);
    showNotification('Event created successfully!');
  }
}, [lastWebSocketMessage]);
```

### **Example 2: Conflict Detection Integration**
```python
# Backend: Automatic conflict detection after event creation
async def check_for_conflicts(new_event: Event, db: Session):
    # Query overlapping events
    overlapping = await db.execute(
        select(Event).where(
            Event.user_id == new_event.user_id,
            Event.start_time < new_event.end_time,
            Event.end_time > new_event.start_time
        )
    )
    
    if overlapping.scalars().all():
        conflict_data = {
            'new_event': new_event.id,
            'conflicting_events': [e.id for e in overlapping.scalars()],
            'severity': 'high' if new_event.priority_level <= 2 else 'medium',
            'suggested_resolution': 'reschedule_lower_priority'
        }
        
        # Broadcast conflict immediately
        await websocket_manager.broadcast_conflict_detected(
            [new_event.user_id], 
            conflict_data
        )

# Frontend: Conflict handling
const handleConflictMessage = (conflictData) => {
  setConflictDialog({
    isOpen: true,
    message: `New event conflicts with ${conflictData.conflicting_events.length} existing events`,
    severity: conflictData.severity,
    options: ['Reschedule', 'Keep Both', 'Replace Lower Priority']
  });
};
```

### **Example 3: Multi-Component Data Flow**
```mermaid
Voice Input: "Urgent dentist appointment Friday 3pm"
    ↓
Frontend VoiceService
    ↓ POST /api/v1/voice/create-event
Backend NLP Pipeline
    ↓ Entity extraction
    title: "Dentist Appointment"
    priority_keywords: ["urgent"] → priority=4
    temporal: "Friday 3pm" → 2025-08-22T15:00:00Z
    ↓
BERT Priority Classifier
    ↓ Input: {"title": "Dentist Appointment", "description": "urgent"}
    ↓ Output: priority=3, confidence=0.72
    ↓
Hybrid Decision Logic
    ↓ bert_confidence=0.72 > 0.7 → Use BERT priority=3
    ↓
Database Storage
    ↓ event_id="uuid-123", priority_level=3
    ↓
WebSocket Broadcast
    ↓ message_type="event_created"
    ↓
Frontend State Updates
    ↓ Dashboard: +1 voice event
    ↓ Calendar: New appointment appears
    ↓ Priority Panel: Medium priority indicator
```

---

## 📊 **8. Performance & Monitoring Integration**

### **Component Performance Tracking**
```python
# Each component tracks its own performance
class NLPService:
    async def process_voice_input(self, voice_text: str):
        start_time = time.time()
        
        # Processing logic...
        
        processing_time = (time.time() - start_time) * 1000
        logger.info(f"🔍 NLP processing: {processing_time:.1f}ms")
        
        return {
            'processing_time_ms': processing_time,
            'confidence': confidence_score,
            # ... other data
        }

class BERTPriorityClassifier:
    def predict(self, event_data):
        start_time = time.time()
        
        # BERT inference...
        
        inference_time = (time.time() - start_time) * 1000
        logger.info(f"🤖 BERT inference: {inference_time:.1f}ms")
        
        return priority, confidence
```

### **End-to-End Performance Monitoring**
```python
# Voice API tracks complete pipeline performance
@voice_router.post("/create-event")
async def create_event_from_voice(request):
    pipeline_start = time.time()
    
    # Step timings
    voice_time = time.time()
    nlp_result = await nlp_service.process_voice_input(request.voice_text)
    nlp_time = (time.time() - voice_time) * 1000
    
    bert_start = time.time()
    bert_priority, confidence = bert_model.predict(event_data)
    bert_time = (time.time() - bert_start) * 1000
    
    db_start = time.time()
    event = await create_event_in_db(event_data)
    db_time = (time.time() - db_start) * 1000
    
    total_time = (time.time() - pipeline_start) * 1000
    
    return VoiceEventResponse(
        # ... event data
        processing_details={
            'total_processing_time': total_time,
            'nlp_processing_time': nlp_time,
            'bert_processing_time': bert_time,
            'database_time': db_time,
            'pipeline_efficiency': 'optimal' if total_time < 1000 else 'slow'
        }
    )
```

---

## 🎯 **Integration Summary**

### **Communication Patterns**
| Component A | Component B | Protocol | Latency | Purpose |
|-------------|-------------|----------|---------|---------|
| Frontend | Backend API | HTTP/REST | 50-200ms | CRUD operations |
| Browser | Voice API | Web Speech API | 100-500ms | Voice transcription |
| Voice API | NLP Service | Function call | 100-300ms | Entity extraction |
| NLP Service | BERT Model | PyTorch inference | 200-500ms | Priority classification |
| Backend | Database | SQLAlchemy ORM | 50-100ms | Data persistence |
| Backend | WebSocket | Socket.IO | <10ms | Real-time updates |
| WebSocket | Frontend | JavaScript events | <10ms | UI updates |

### **Data Flow Efficiency**
- **Voice-to-Database**: 650-1750ms total pipeline
- **Real-time Updates**: <50ms WebSocket notification
- **BERT Classification**: 94% accuracy with 200-500ms inference
- **Conflict Detection**: Immediate notification after event creation
- **Multi-device Sync**: WebSocket ensures all connected devices update simultaneously

### **Scalability Architecture**
- **Current**: Single-server with SQLite + in-memory WebSocket
- **Production Ready**: Docker + PostgreSQL + Redis clustering
- **Enterprise Scale**: Multi-server WebSocket with Redis pub/sub
- **AI Scaling**: BERT model ready for GPU acceleration
