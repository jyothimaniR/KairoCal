"""
Advanced WebSocket Connection Manager for KairoCal
Manages user connections across multiple devices with enterprise-grade features
"""

import asyncio
import logging
import time
from typing import Dict, Set, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json

# import aioredis  # Temporarily disabled for testing
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class ConnectionStatus(Enum):
    """Connection status enumeration"""
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTING = "disconnecting"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"

class DeviceType(Enum):
    """Device type enumeration"""
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    WEB = "web"
    UNKNOWN = "unknown"

@dataclass
class DeviceInfo:
    """Device information"""
    device_id: str
    device_type: DeviceType
    user_agent: str
    ip_address: str
    platform: str
    browser: str
    version: str
    screen_resolution: Optional[str] = None
    timezone: Optional[str] = None

@dataclass
class ConnectionInfo:
    """Connection information"""
    session_id: str
    user_id: int
    device_info: DeviceInfo
    connected_at: datetime
    last_activity: datetime
    status: ConnectionStatus
    reconnect_count: int = 0
    latency: float = 0.0
    message_count: int = 0

@dataclass
class QueuedMessage:
    """Queued message for offline users"""
    message_id: str
    user_id: int
    message_type: str
    payload: Dict[str, Any]
    created_at: datetime
    expires_at: datetime
    priority: int = 1  # 1=high, 2=medium, 3=low
    attempts: int = 0
    max_attempts: int = 3

class AdvancedConnectionManager:
    """
    Enterprise-grade connection manager for WebSocket clients
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client: Optional[Any] = None  # Temporarily disabled
        
        # Connection tracking
        self.connections: Dict[str, ConnectionInfo] = {}  # session_id -> ConnectionInfo
        self.user_sessions: Dict[int, Set[str]] = defaultdict(set)  # user_id -> set of session_ids
        self.device_sessions: Dict[str, str] = {}  # device_id -> session_id
        
        # User presence tracking
        self.user_presence: Dict[int, Dict[str, Any]] = {}  # user_id -> presence info
        
        # Message queuing for offline users
        self.message_queues: Dict[int, deque] = defaultdict(deque)  # user_id -> message queue
        self.max_queue_size = 100
        self.message_retention_hours = 24
        
        # Connection metrics
        self.connection_metrics = {
            'total_connections': 0,
            'peak_connections': 0,
            'reconnections': 0,
            'failed_connections': 0,
            'messages_queued': 0,
            'messages_delivered': 0
        }
        
        # Rate limiting
        self.rate_limits: Dict[str, deque] = defaultdict(deque)  # session_id -> timestamps
        self.max_messages_per_minute = 60
        
        # Start background tasks
        self.cleanup_task: Optional[asyncio.Task] = None
        self.metrics_task: Optional[asyncio.Task] = None
        
    async def initialize(self):
        """Initialize the connection manager"""
        try:
            # Initialize Redis connection - temporarily disabled
            # self.redis_client = aioredis.from_url(
            #     self.redis_url,
            #     encoding="utf-8",
            #     decode_responses=True,
            #     socket_keepalive=True,
            #     health_check_interval=30
            # )
            
            # Test Redis connection
            await self.redis_client.ping()
            logger.info("✅ Connection Manager: Redis initialized")
            
            # Start background tasks
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
            self.metrics_task = asyncio.create_task(self._metrics_loop())
            
            logger.info("✅ Connection Manager: Initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Connection Manager initialization failed: {e}")
            raise
    
    async def add_connection(
        self, 
        session_id: str, 
        user_id: int, 
        device_info: DeviceInfo
    ) -> ConnectionInfo:
        """Add a new connection"""
        try:
            # Check for existing connection from same device
            existing_session = self.device_sessions.get(device_info.device_id)
            if existing_session and existing_session in self.connections:
                # Disconnect old session
                await self.remove_connection(existing_session, reason="device_reconnection")
            
            # Create connection info
            connection = ConnectionInfo(
                session_id=session_id,
                user_id=user_id,
                device_info=device_info,
                connected_at=datetime.now(),
                last_activity=datetime.now(),
                status=ConnectionStatus.CONNECTED
            )
            
            # Store connection
            self.connections[session_id] = connection
            self.user_sessions[user_id].add(session_id)
            self.device_sessions[device_info.device_id] = session_id
            
            # Update metrics
            self.connection_metrics['total_connections'] += 1
            current_connections = len(self.connections)
            if current_connections > self.connection_metrics['peak_connections']:
                self.connection_metrics['peak_connections'] = current_connections
            
            # Update user presence
            await self._update_user_presence(user_id)
            
            # Store in Redis for persistence
            if self.redis_client:
                await self.redis_client.hset(
                    f"connection:{session_id}",
                    mapping={
                        "user_id": user_id,
                        "device_id": device_info.device_id,
                        "connected_at": connection.connected_at.isoformat(),
                        "status": connection.status.value
                    }
                )
            
            # Deliver queued messages
            await self._deliver_queued_messages(user_id, session_id)
            
            logger.info(f"✅ Connection added: {session_id} (User: {user_id}, Device: {device_info.device_type.value})")
            return connection
            
        except Exception as e:
            logger.error(f"❌ Failed to add connection {session_id}: {e}")
            raise
    
    async def remove_connection(self, session_id: str, reason: str = "normal_disconnect"):
        """Remove a connection"""
        try:
            connection = self.connections.get(session_id)
            if not connection:
                return
            
            user_id = connection.user_id
            device_id = connection.device_info.device_id
            
            # Update status
            connection.status = ConnectionStatus.DISCONNECTED
            
            # Remove from tracking
            self.connections.pop(session_id, None)
            self.user_sessions[user_id].discard(session_id)
            if not self.user_sessions[user_id]:
                self.user_sessions.pop(user_id, None)
            
            if self.device_sessions.get(device_id) == session_id:
                self.device_sessions.pop(device_id, None)
            
            # Update user presence
            await self._update_user_presence(user_id)
            
            # Clean up Redis
            if self.redis_client:
                await self.redis_client.delete(f"connection:{session_id}")
            
            logger.info(f"👋 Connection removed: {session_id} (Reason: {reason})")
            
        except Exception as e:
            logger.error(f"❌ Failed to remove connection {session_id}: {e}")
    
    async def update_activity(self, session_id: str, latency: Optional[float] = None):
        """Update connection activity"""
        try:
            connection = self.connections.get(session_id)
            if connection:
                connection.last_activity = datetime.now()
                if latency is not None:
                    connection.latency = latency
                connection.message_count += 1
                
        except Exception as e:
            logger.error(f"❌ Failed to update activity for {session_id}: {e}")
    
    async def get_user_connections(self, user_id: int) -> List[ConnectionInfo]:
        """Get all connections for a user"""
        try:
            session_ids = self.user_sessions.get(user_id, set())
            return [self.connections[sid] for sid in session_ids if sid in self.connections]
        except Exception as e:
            logger.error(f"❌ Failed to get user connections for {user_id}: {e}")
            return []
    
    async def is_user_online(self, user_id: int) -> bool:
        """Check if user is online"""
        return user_id in self.user_sessions and len(self.user_sessions[user_id]) > 0
    
    async def get_online_users(self) -> List[int]:
        """Get list of online user IDs"""
        return list(self.user_sessions.keys())
    
    async def queue_message(self, user_id: int, message: QueuedMessage):
        """Queue a message for offline user"""
        try:
            # Check if user is online
            if await self.is_user_online(user_id):
                return False  # User is online, don't queue
            
            # Add to queue
            queue = self.message_queues[user_id]
            
            # Remove expired messages and maintain queue size
            now = datetime.now()
            while queue and (queue[0].expires_at < now or len(queue) >= self.max_queue_size):
                queue.popleft()
            
            queue.append(message)
            self.connection_metrics['messages_queued'] += 1
            
            # Store in Redis for persistence
            if self.redis_client:
                await self.redis_client.lpush(
                    f"message_queue:{user_id}",
                    json.dumps(asdict(message), default=str)
                )
                await self.redis_client.expire(f"message_queue:{user_id}", 86400)  # 24 hours
            
            logger.info(f"📦 Message queued for user {user_id}: {message.message_type}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to queue message for user {user_id}: {e}")
            return False
    
    async def _deliver_queued_messages(self, user_id: int, session_id: str):
        """Deliver queued messages to newly connected user"""
        try:
            # Get messages from local queue
            queue = self.message_queues.get(user_id, deque())
            now = datetime.now()
            
            # Also get messages from Redis
            if self.redis_client:
                redis_messages = await self.redis_client.lrange(f"message_queue:{user_id}", 0, -1)
                for msg_data in redis_messages:
                    try:
                        msg_dict = json.loads(msg_data)
                        # Convert back to QueuedMessage
                        msg_dict['created_at'] = datetime.fromisoformat(msg_dict['created_at'])
                        msg_dict['expires_at'] = datetime.fromisoformat(msg_dict['expires_at'])
                        message = QueuedMessage(**msg_dict)
                        if message.expires_at > now:
                            queue.append(message)
                    except Exception as e:
                        logger.error(f"❌ Failed to parse queued message: {e}")
            
            # Deliver valid messages
            delivered_count = 0
            while queue:
                message = queue.popleft()
                if message.expires_at > now:
                    # TODO: Emit message to session
                    # This would be implemented by the socket server
                    delivered_count += 1
                    self.connection_metrics['messages_delivered'] += 1
            
            # Clear Redis queue
            if self.redis_client and delivered_count > 0:
                await self.redis_client.delete(f"message_queue:{user_id}")
            
            if delivered_count > 0:
                logger.info(f"📬 Delivered {delivered_count} queued messages to user {user_id}")
                
        except Exception as e:
            logger.error(f"❌ Failed to deliver queued messages for user {user_id}: {e}")
    
    async def _update_user_presence(self, user_id: int):
        """Update user presence information"""
        try:
            connections = await self.get_user_connections(user_id)
            
            if connections:
                # User is online
                device_types = [conn.device_info.device_type.value for conn in connections]
                last_activity = max(conn.last_activity for conn in connections)
                
                presence = {
                    'status': 'online',
                    'last_seen': last_activity.isoformat(),
                    'device_count': len(connections),
                    'device_types': list(set(device_types)),
                    'updated_at': datetime.now().isoformat()
                }
            else:
                # User is offline
                presence = {
                    'status': 'offline',
                    'last_seen': datetime.now().isoformat(),
                    'device_count': 0,
                    'device_types': [],
                    'updated_at': datetime.now().isoformat()
                }
            
            self.user_presence[user_id] = presence
            
            # Store in Redis
            if self.redis_client:
                await self.redis_client.hset(
                    f"presence:{user_id}",
                    mapping=presence
                )
                await self.redis_client.expire(f"presence:{user_id}", 3600)  # 1 hour
                
        except Exception as e:
            logger.error(f"❌ Failed to update presence for user {user_id}: {e}")
    
    async def get_user_presence(self, user_id: int) -> Dict[str, Any]:
        """Get user presence information"""
        try:
            # Try local cache first
            if user_id in self.user_presence:
                return self.user_presence[user_id]
            
            # Try Redis
            if self.redis_client:
                presence = await self.redis_client.hgetall(f"presence:{user_id}")
                if presence:
                    return presence
            
            # Default to offline
            return {
                'status': 'offline',
                'last_seen': None,
                'device_count': 0,
                'device_types': [],
                'updated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get presence for user {user_id}: {e}")
            return {'status': 'unknown'}
    
    async def check_rate_limit(self, session_id: str) -> bool:
        """Check rate limiting for a session"""
        try:
            now = time.time()
            timestamps = self.rate_limits[session_id]
            
            # Remove timestamps older than 1 minute
            while timestamps and now - timestamps[0] > 60:
                timestamps.popleft()
            
            # Check if limit exceeded
            if len(timestamps) >= self.max_messages_per_minute:
                return False
            
            # Add current timestamp
            timestamps.append(now)
            return True
            
        except Exception as e:
            logger.error(f"❌ Rate limit check failed for {session_id}: {e}")
            return True  # Allow on error
    
    async def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        try:
            online_users = len(self.user_sessions)
            total_connections = len(self.connections)
            
            # Calculate average latency
            latencies = [conn.latency for conn in self.connections.values() if conn.latency > 0]
            avg_latency = sum(latencies) / len(latencies) if latencies else 0
            
            # Device type distribution
            device_types = {}
            for conn in self.connections.values():
                device_type = conn.device_info.device_type.value
                device_types[device_type] = device_types.get(device_type, 0) + 1
            
            return {
                'total_connections': total_connections,
                'online_users': online_users,
                'peak_connections': self.connection_metrics['peak_connections'],
                'reconnections': self.connection_metrics['reconnections'],
                'failed_connections': self.connection_metrics['failed_connections'],
                'messages_queued': self.connection_metrics['messages_queued'],
                'messages_delivered': self.connection_metrics['messages_delivered'],
                'average_latency_ms': round(avg_latency, 2),
                'device_distribution': device_types,
                'redis_connected': self.redis_client is not None
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get connection stats: {e}")
            return {}
    
    async def _cleanup_loop(self):
        """Background cleanup task"""
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                
                now = datetime.now()
                inactive_sessions = []
                
                # Find inactive connections (no activity for 30 minutes)
                for session_id, connection in self.connections.items():
                    if now - connection.last_activity > timedelta(minutes=30):
                        inactive_sessions.append(session_id)
                
                # Remove inactive sessions
                for session_id in inactive_sessions:
                    await self.remove_connection(session_id, "inactive_timeout")
                
                # Clean up message queues
                for user_id, queue in list(self.message_queues.items()):
                    while queue and queue[0].expires_at < now:
                        queue.popleft()
                    if not queue:
                        self.message_queues.pop(user_id, None)
                
                # Clean up rate limits
                current_time = time.time()
                for session_id, timestamps in list(self.rate_limits.items()):
                    while timestamps and current_time - timestamps[0] > 60:
                        timestamps.popleft()
                    if not timestamps:
                        self.rate_limits.pop(session_id, None)
                
                logger.debug(f"🧹 Cleanup completed: removed {len(inactive_sessions)} inactive sessions")
                
            except Exception as e:
                logger.error(f"❌ Cleanup loop error: {e}")
    
    async def _metrics_loop(self):
        """Background metrics collection task"""
        while True:
            try:
                await asyncio.sleep(60)  # Run every minute
                
                # Store metrics in Redis
                if self.redis_client:
                    stats = await self.get_connection_stats()
                    await self.redis_client.hset(
                        "connection_metrics",
                        mapping={
                            **stats,
                            'timestamp': datetime.now().isoformat()
                        }
                    )
                    await self.redis_client.expire("connection_metrics", 86400)  # 24 hours
                
            except Exception as e:
                logger.error(f"❌ Metrics loop error: {e}")
    
    async def shutdown(self):
        """Shutdown the connection manager"""
        try:
            # Cancel background tasks
            if self.cleanup_task:
                self.cleanup_task.cancel()
            if self.metrics_task:
                self.metrics_task.cancel()
            
            # Close Redis connection
            if self.redis_client:
                await self.redis_client.close()
            
            logger.info("🛑 Connection Manager: Shutdown completed")
            
        except Exception as e:
            logger.error(f"❌ Shutdown error: {e}")

# Global instance
connection_manager = AdvancedConnectionManager()

async def get_connection_manager() -> AdvancedConnectionManager:
    """Get the global connection manager instance"""
    return connection_manager
