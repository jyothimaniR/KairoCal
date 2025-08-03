"""
Ultimate Enterprise-Grade WebSocket Server for KairoCal
Implements Socket.IO with WebTransport fallback, Redis clustering, and enterprise security
"""

import asyncio
import logging
import time
import json
from typing import Dict, List, Set, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

import socketio
import jwt
# import redis.asyncio as redis  # Temporarily disabled for testing
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError

from .connection_manager import (
    AdvancedConnectionManager, 
    DeviceInfo, 
    DeviceType, 
    ConnectionInfo, 
    QueuedMessage,
    get_connection_manager
)
from .redis_adapter import (
    RedisAdapter, 
    BroadcastMessage, 
    MessageType, 
    BroadcastScope,
    get_redis_adapter
)

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class UserSession:
    """User session data structure"""
    user_id: int
    username: str
    email: str
    connected_at: datetime
    last_activity: datetime
    device_id: str
    device_type: str
    ip_address: str
    user_agent: str

@dataclass
class ConnectionMetrics:
    """Connection metrics for monitoring"""
    total_connections: int = 0
    active_users: int = 0
    messages_sent: int = 0
    messages_received: int = 0
    errors: int = 0
    avg_latency: float = 0.0

class WebSocketMessage(BaseModel):
    """WebSocket message structure"""
    type: str
    data: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[int] = None
    room: Optional[str] = None
    
class UltimateSocketServer:
    """
    Enterprise-grade Socket.IO server with Redis clustering and advanced features
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379", secret_key: str = "your-secret-key"):
        self.secret_key = secret_key
        self.redis_url = redis_url
        
        # Initialize Redis connection
        self.redis_client: Optional[Any] = None  # Temporarily disabled
        
        # User session management
        self.user_sessions: Dict[str, UserSession] = {}  # session_id -> UserSession
        self.user_connections: Dict[int, Set[str]] = {}  # user_id -> set of session_ids
        self.connection_metrics = ConnectionMetrics()
        
        # Rate limiting
        self.rate_limits: Dict[str, List[float]] = {}  # session_id -> list of timestamps
        self.max_messages_per_minute = 100
        
        # Initialize Socket.IO server with enterprise configuration
        self.sio = socketio.AsyncServer(
            async_mode='asgi',
            cors_allowed_origins=['http://localhost:5173', 'http://localhost:3000'],
            cors_credentials=True,
            ping_timeout=60,
            ping_interval=25,
            max_http_buffer_size=1024 * 1024,  # 1MB
            logger=logger,
            engineio_logger=logger
        )
        
        # Register event handlers
        self._register_handlers()
        
    async def initialize_redis(self):
        """Initialize connection manager and Redis adapter"""
        try:
            # Initialize connection manager
            self.connection_manager = await get_connection_manager()
            await self.connection_manager.initialize()
            logger.info("✅ Connection Manager initialized")
            
            # Initialize Redis adapter
            self.redis_adapter = await get_redis_adapter()
            await self.redis_adapter.initialize()
            logger.info("✅ Redis Adapter initialized")
            
            # Register Redis message handlers
            await self._setup_redis_handlers()
            
            # Start background tasks
            asyncio.create_task(self._cleanup_inactive_connections())
            asyncio.create_task(self._send_metrics_to_redis())
            
        except Exception as e:
            logger.error(f"❌ Component initialization failed: {e}")
            raise
    
    async def _setup_redis_handlers(self):
        """Setup Redis message handlers for multi-server communication"""
        try:
            # Register handlers for different message types
            await self.redis_adapter.register_handler(
                MessageType.EVENT_CREATED, self._handle_event_created_broadcast
            )
            await self.redis_adapter.register_handler(
                MessageType.EVENT_UPDATED, self._handle_event_updated_broadcast
            )
            await self.redis_adapter.register_handler(
                MessageType.CONFLICT_DETECTED, self._handle_conflict_broadcast
            )
            await self.redis_adapter.register_handler(
                MessageType.REMINDER_NOTIFICATION, self._handle_reminder_broadcast
            )
            await self.redis_adapter.register_handler(
                MessageType.PRIORITY_ALERT, self._handle_priority_alert_broadcast
            )
            await self.redis_adapter.register_handler(
                MessageType.VOICE_TRANSCRIPTION, self._handle_voice_transcription_broadcast
            )
            
            logger.info("✅ Redis message handlers registered")
            
        except Exception as e:
            logger.error(f"❌ Redis handlers setup failed: {e}")
    
    # Redis broadcast handlers
    async def _handle_event_created_broadcast(self, message: BroadcastMessage):
        """Handle event created broadcast from Redis"""
        try:
            user_id = message.payload.get('user_id')
            if user_id:
                await self._emit_to_user(user_id, 'event_created', message.payload)
        except Exception as e:
            logger.error(f"❌ Event created broadcast failed: {e}")
    
    async def _handle_event_updated_broadcast(self, message: BroadcastMessage):
        """Handle event updated broadcast from Redis"""
        try:
            user_id = message.payload.get('user_id')
            if user_id:
                await self._emit_to_user(user_id, 'event_updated', message.payload)
        except Exception as e:
            logger.error(f"❌ Event updated broadcast failed: {e}")
    
    async def _handle_conflict_broadcast(self, message: BroadcastMessage):
        """Handle conflict detection broadcast from Redis"""
        try:
            affected_users = message.payload.get('affected_users', [])
            for user_id in affected_users:
                await self._emit_to_user(user_id, 'conflict_detected', message.payload)
        except Exception as e:
            logger.error(f"❌ Conflict broadcast failed: {e}")
    
    async def _handle_reminder_broadcast(self, message: BroadcastMessage):
        """Handle reminder notification broadcast from Redis"""
        try:
            user_id = message.payload.get('user_id')
            if user_id:
                await self._emit_to_user(user_id, 'reminder_notification', message.payload)
        except Exception as e:
            logger.error(f"❌ Reminder broadcast failed: {e}")
    
    async def _handle_priority_alert_broadcast(self, message: BroadcastMessage):
        """Handle priority alert broadcast from Redis"""
        try:
            user_id = message.payload.get('user_id')
            if user_id:
                await self._emit_to_user(user_id, 'priority_alert', message.payload)
        except Exception as e:
            logger.error(f"❌ Priority alert broadcast failed: {e}")
    
    async def _handle_voice_transcription_broadcast(self, message: BroadcastMessage):
        """Handle voice transcription broadcast from Redis"""
        try:
            user_id = message.payload.get('user_id')
            if user_id:
                await self._emit_to_user(user_id, 'voice_transcription', message.payload)
        except Exception as e:
            logger.error(f"❌ Voice transcription broadcast failed: {e}")
    
    async def _emit_to_user(self, user_id: int, event: str, data: Dict[str, Any]):
        """Emit message to all sessions of a specific user"""
        try:
            if not self.connection_manager:
                return
            
            connections = await self.connection_manager.get_user_connections(user_id)
            for connection in connections:
                await self.sio.emit(event, data, room=connection.session_id)
                
        except Exception as e:
            logger.error(f"❌ Emit to user {user_id} failed: {e}")
    
    def _register_handlers(self):
        """Register all Socket.IO event handlers"""
        
        @self.sio.event
        async def connect(sid: str, environ: dict, auth: dict):
            """Handle client connection with enhanced connection management"""
            try:
                # Extract token from auth
                token = auth.get('token') if auth else None
                if not token:
                    logger.warning(f"🔒 Connection denied - No token provided: {sid}")
                    return False
                
                # Verify JWT token
                user_data = await self._verify_jwt_token(token)
                if not user_data:
                    logger.warning(f"🔒 Connection denied - Invalid token: {sid}")
                    return False
                
                # Extract device information from auth and environ
                device_info_data = auth.get('deviceInfo', {})
                device_info = DeviceInfo(
                    device_id=device_info_data.get('deviceId', f"device_{sid[:8]}"),
                    device_type=DeviceType(device_info_data.get('deviceType', 'unknown')),
                    user_agent=environ.get('HTTP_USER_AGENT', 'unknown'),
                    ip_address=environ.get('REMOTE_ADDR', 'unknown'),
                    platform=device_info_data.get('platform', 'unknown'),
                    browser=device_info_data.get('browser', 'unknown'),
                    version=device_info_data.get('version', '1.0'),
                    screen_resolution=device_info_data.get('screenResolution'),
                    timezone=device_info_data.get('timezone')
                )
                
                # Add connection to manager
                if self.connection_manager:
                    connection = await self.connection_manager.add_connection(
                        session_id=sid,
                        user_id=user_data['user_id'],
                        device_info=device_info
                    )
                    
                    # Store user session for local access
                    self.user_sessions[sid] = UserSession(
                        user_id=user_data['user_id'],
                        username=user_data.get('username', 'unknown'),
                        email=user_data.get('email', 'unknown'),
                        connected_at=connection.connected_at,
                        last_activity=connection.last_activity,
                        device_id=device_info.device_id,
                        device_type=device_info.device_type.value,
                        ip_address=device_info.ip_address,
                        user_agent=device_info.user_agent
                    )
                
                # Update metrics
                self.connection_metrics.total_connections += 1
                self.connection_metrics.active_users = len(set(
                    session.user_id for session in self.user_sessions.values()
                ))
                
                # Broadcast user presence update
                if self.redis_adapter:
                    await self.redis_adapter.broadcast_user_presence(
                        user_data['user_id'],
                        {
                            'status': 'online',
                            'device_type': device_info.device_type.value,
                            'last_seen': datetime.now().isoformat()
                        }
                    )
                
                logger.info(f"✅ User connected: {user_data['username']} ({sid})")
                return True
                
            except Exception as e:
                logger.error(f"❌ Connection error: {e}")
                return False
        
        @self.sio.event
        async def disconnect(sid: str):
            """Handle client disconnection with enhanced cleanup"""
            try:
                # Get session info
                session = self.user_sessions.get(sid)
                if not session:
                    return
                
                user_id = session.user_id
                
                # Remove from connection manager
                if self.connection_manager:
                    await self.connection_manager.remove_connection(sid, "normal_disconnect")
                
                # Clean up local session
                self.user_sessions.pop(sid, None)
                
                # Update metrics
                self.connection_metrics.total_connections = max(0, self.connection_metrics.total_connections - 1)
                self.connection_metrics.active_users = len(set(
                    session.user_id for session in self.user_sessions.values()
                ))
                
                # Check if user is still online on other devices
                user_still_online = any(
                    s.user_id == user_id for s in self.user_sessions.values()
                )
                
                # Broadcast presence update if user is now offline
                if not user_still_online and self.redis_adapter:
                    await self.redis_adapter.broadcast_user_presence(
                        user_id,
                        {
                            'status': 'offline',
                            'last_seen': datetime.now().isoformat()
                        }
                    )
                
                logger.info(f"👋 User disconnected: {session.username} ({sid})")
                
            except Exception as e:
                logger.error(f"❌ Disconnect error: {e}")
        
        @self.sio.event
        async def disconnect(sid: str):
            """Handle client disconnection"""
            try:
                session = self.user_sessions.get(sid)
                if not session:
                    return
                
                user_id = session.user_id
                
                # Remove from user connections
                if user_id in self.user_connections:
                    self.user_connections[user_id].discard(sid)
                    if not self.user_connections[user_id]:
                        del self.user_connections[user_id]
                        # User completely offline
                        await self._broadcast_user_presence(user_id, 'offline')
                
                # Remove session
                del self.user_sessions[sid]
                
                logger.info(f"👋 User disconnected: {session.username} ({user_id})")
                
            except Exception as e:
                logger.error(f"❌ Disconnection error: {e}")
        
        @self.sio.event
        async def heartbeat(sid: str, data: dict):
            """Handle client heartbeat for connection monitoring"""
            try:
                session = self.user_sessions.get(sid)
                if session:
                    session.last_activity = datetime.now()
                    
                    # Send heartbeat response with latency
                    await self.sio.emit('heartbeat_response', {
                        'server_time': datetime.now().isoformat(),
                        'latency': data.get('timestamp')
                    }, room=sid)
                    
            except Exception as e:
                logger.error(f"❌ Heartbeat error: {e}")
        
        @self.sio.event
        async def subscribe_events(sid: str, data: dict):
            """Subscribe to specific event types"""
            try:
                session = self.user_sessions.get(sid)
                if not session:
                    return
                
                event_types = data.get('event_types', [])
                
                for event_type in event_types:
                    room_name = f"events_{event_type}_{session.user_id}"
                    await self.sio.enter_room(sid, room_name)
                
                await self.sio.emit('subscription_confirmed', {
                    'event_types': event_types
                }, room=sid)
                
            except Exception as e:
                logger.error(f"❌ Event subscription error: {e}")
        
        @self.sio.event
        async def voice_processing_status(sid: str, data: dict):
            """Handle voice processing status updates"""
            try:
                session = self.user_sessions.get(sid)
                if not session:
                    return
                
                if not await self._check_rate_limit(sid):
                    return
                
                # Broadcast voice processing status to user's other devices
                await self.sio.emit('voice_status_update', {
                    'status': data.get('status'),
                    'progress': data.get('progress', 0),
                    'device_id': session.device_id,
                    'timestamp': datetime.now().isoformat()
                }, room=f"user_{session.user_id}")
                
                self.connection_metrics.messages_received += 1
                
            except Exception as e:
                logger.error(f"❌ Voice processing status error: {e}")
    
    async def _verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and extract user data"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Verify token hasn't expired
            if payload.get('exp', 0) < time.time():
                return None
            
            return {
                'user_id': payload.get('user_id'),
                'username': payload.get('username'),
                'email': payload.get('email')
            }
            
        except jwt.InvalidTokenError:
            return None
    
    async def _check_rate_limit(self, sid: str) -> bool:
        """Check rate limiting for user messages"""
        try:
            now = time.time()
            
            if sid not in self.rate_limits:
                self.rate_limits[sid] = []
            
            # Remove old timestamps (older than 1 minute)
            self.rate_limits[sid] = [
                ts for ts in self.rate_limits[sid] 
                if now - ts < 60
            ]
            
            # Check if user exceeded rate limit
            if len(self.rate_limits[sid]) >= self.max_messages_per_minute:
                await self.sio.emit('rate_limit_exceeded', {
                    'message': 'Too many messages. Please slow down.',
                    'retry_after': 60
                }, room=sid)
                return False
            
            # Add current timestamp
            self.rate_limits[sid].append(now)
            return True
            
        except Exception as e:
            logger.error(f"❌ Rate limit check error: {e}")
            return True  # Allow on error
    
    async def _broadcast_user_presence(self, user_id: int, status: str, exclude_sid: str = None):
        """Broadcast user presence status to other users"""
        try:
            presence_data = {
                'user_id': user_id,
                'status': status,
                'timestamp': datetime.now().isoformat(),
                'active_devices': len(self.user_connections.get(user_id, set()))
            }
            
            # Broadcast to user's connections
            room = f"user_{user_id}"
            await self.sio.emit('user_presence', presence_data, room=room, skip_sid=exclude_sid)
            
        except Exception as e:
            logger.error(f"❌ User presence broadcast error: {e}")
    
    # Public methods for broadcasting events
    
    async def broadcast_event_created(self, event_data: Dict[str, Any]):
        """Broadcast new event creation to user"""
        try:
            user_id = event_data.get('user_id')
            if not user_id:
                return
            
            message = {
                'type': 'event_created',
                'event': event_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Broadcast to user's devices
            await self.sio.emit('event_created', message, room=f"user_{user_id}")
            
            # Publish to Redis for other servers
            if self.redis_client:
                await self.redis_client.publish('kairocal:events', json.dumps(message))
            
            self.connection_metrics.messages_sent += 1
            logger.info(f"📅 Event created broadcast sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Event creation broadcast error: {e}")
    
    async def broadcast_priority_classified(self, user_id: int, priority_data: Dict[str, Any]):
        """Broadcast BERT priority classification results"""
        try:
            message = {
                'type': 'priority_classified',
                'priority': priority_data.get('priority'),
                'confidence': priority_data.get('confidence'),
                'event_text': priority_data.get('event_text'),
                'timestamp': datetime.now().isoformat()
            }
            
            await self.sio.emit('priority_classified', message, room=f"user_{user_id}")
            
            if self.redis_client:
                priority_message = {**message, 'user_id': user_id}
                await self.redis_client.publish('kairocal:priorities', json.dumps(priority_message))
            
            self.connection_metrics.messages_sent += 1
            
        except Exception as e:
            logger.error(f"❌ Priority classification broadcast error: {e}")
    
    async def broadcast_conflict_detected(self, affected_users: List[int], conflict_data: Dict[str, Any]):
        """Broadcast conflict detection to affected users"""
        try:
            message = {
                'type': 'conflict_detected',
                'conflict': conflict_data,
                'severity': conflict_data.get('severity', 'medium'),
                'timestamp': datetime.now().isoformat()
            }
            
            for user_id in affected_users:
                await self.sio.emit('conflict_detected', message, room=f"user_{user_id}")
            
            if self.redis_client:
                redis_message = {**message, 'affected_users': affected_users}
                await self.redis_client.publish('kairocal:conflicts', json.dumps(redis_message))
            
            self.connection_metrics.messages_sent += len(affected_users)
            
        except Exception as e:
            logger.error(f"❌ Conflict detection broadcast error: {e}")
    
    async def _broadcast_event_update(self, data: Dict[str, Any]):
        """Handle event update broadcasts from Redis"""
        try:
            user_id = data.get('user_id')
            if user_id and user_id in self.user_connections:
                await self.sio.emit('event_updated', data, room=f"user_{user_id}")
        except Exception as e:
            logger.error(f"❌ Event update broadcast error: {e}")
    
    async def _broadcast_conflict_detection(self, data: Dict[str, Any]):
        """Handle conflict detection broadcasts from Redis"""
        try:
            affected_users = data.get('affected_users', [])
            for user_id in affected_users:
                if user_id in self.user_connections:
                    await self.sio.emit('conflict_detected', data, room=f"user_{user_id}")
        except Exception as e:
            logger.error(f"❌ Conflict broadcast error: {e}")
    
    async def _broadcast_priority_update(self, data: Dict[str, Any]):
        """Handle priority update broadcasts from Redis"""
        try:
            user_id = data.get('user_id')
            if user_id and user_id in self.user_connections:
                await self.sio.emit('priority_classified', data, room=f"user_{user_id}")
        except Exception as e:
            logger.error(f"❌ Priority broadcast error: {e}")
    
    async def _broadcast_user_update(self, data: Dict[str, Any]):
        """Handle user update broadcasts from Redis"""
        try:
            user_id = data.get('user_id')
            if user_id and user_id in self.user_connections:
                await self.sio.emit('user_updated', data, room=f"user_{user_id}")
        except Exception as e:
            logger.error(f"❌ User update broadcast error: {e}")
    
    async def get_connection_stats(self) -> Dict[str, Any]:
        """Get current connection statistics"""
        try:
            return {
                'total_connections': self.connection_metrics.total_connections,
                'active_users': self.connection_metrics.active_users,
                'messages_sent': self.connection_metrics.messages_sent,
                'messages_received': self.connection_metrics.messages_received,
                'errors': self.connection_metrics.errors,
                'avg_latency': self.connection_metrics.avg_latency,
                'uptime': 'calculated_dynamically',
                'redis_connected': self.redis_client is not None,
                'active_sessions': len(self.user_sessions)
            }
        except Exception as e:
            logger.error(f"❌ Stats retrieval error: {e}")
            return {}
    
    async def cleanup(self):
        """Cleanup resources on shutdown"""
        try:
            if self.redis_client:
                await self.redis_client.close()
            logger.info("🧹 WebSocket server cleanup completed")
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")

# Global instance
ultimate_socket_server = UltimateSocketServer()

async def get_socket_server() -> UltimateSocketServer:
    """Get the global socket server instance"""
    return ultimate_socket_server
