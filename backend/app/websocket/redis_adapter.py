"""
Redis Adapter for Multi-Server WebSocket Broadcasting
Enables horizontal scaling with Redis pub/sub and message broadcasting
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable, Set
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# import aioredis  # Temporarily disabled for testing
# from aioredis.client import PubSub

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """Message types for Redis broadcasting"""
    EVENT_CREATED = "event_created"
    EVENT_UPDATED = "event_updated"
    EVENT_DELETED = "event_deleted"
    REMINDER_NOTIFICATION = "reminder_notification"
    CONFLICT_DETECTED = "conflict_detected"
    USER_PRESENCE = "user_presence"
    SYSTEM_BROADCAST = "system_broadcast"
    PRIORITY_ALERT = "priority_alert"
    VOICE_TRANSCRIPTION = "voice_transcription"

class BroadcastScope(Enum):
    """Broadcast scope enumeration"""
    USER = "user"          # Single user
    USERS = "users"        # Multiple specific users
    ALL = "all"           # All connected users
    ROOM = "room"         # Users in a specific room/group

@dataclass
class BroadcastMessage:
    """Message for Redis broadcasting"""
    message_id: str
    message_type: MessageType
    scope: BroadcastScope
    payload: Dict[str, Any]
    sender_server_id: str
    timestamp: datetime
    target_users: Optional[List[int]] = None
    room_id: Optional[str] = None
    priority: int = 1  # 1=high, 2=medium, 3=low
    ttl_seconds: int = 300  # 5 minutes default

class RedisAdapter:
    """
    Redis adapter for multi-server WebSocket message broadcasting
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379", server_id: Optional[str] = None):
        self.redis_url = redis_url
        self.server_id = server_id or f"kairo-server-{uuid.uuid4().hex[:8]}"
        
        # Redis connections
        self.redis_client: Optional[Any] = None  # Temporarily disabled
        self.pubsub_client: Optional[Any] = None
        self.pubsub: Optional[Any] = None
        
        # Channel configuration
        self.broadcast_channel = "kairo:broadcast"
        self.presence_channel = "kairo:presence"
        self.system_channel = "kairo:system"
        
        # Message handlers
        self.message_handlers: Dict[MessageType, List[Callable]] = {}
        
        # Server registry
        self.server_registry: Set[str] = set()
        
        # Background tasks
        self.subscriber_task: Optional[asyncio.Task] = None
        self.heartbeat_task: Optional[asyncio.Task] = None
        
        # Metrics
        self.metrics = {
            'messages_sent': 0,
            'messages_received': 0,
            'broadcast_errors': 0,
            'servers_discovered': 0,
            'last_heartbeat': None
        }
    
    async def initialize(self):
        """Initialize Redis adapter"""
        try:
            # Initialize Redis connections - temporarily disabled
            # self.redis_client = aioredis.from_url(
            #     self.redis_url,
            #     encoding="utf-8",
            #     decode_responses=True,
            #     socket_keepalive=True,
            #     health_check_interval=30
            # )
            
            # self.pubsub_client = aioredis.from_url(
            #     self.redis_url,
            #     encoding="utf-8",
            #     decode_responses=True
            # )
            
            # Test connections
            await self.redis_client.ping()
            await self.pubsub_client.ping()
            
            # Initialize pub/sub
            self.pubsub = self.pubsub_client.pubsub()
            await self.pubsub.subscribe(
                self.broadcast_channel,
                self.presence_channel,
                self.system_channel
            )
            
            # Register this server
            await self._register_server()
            
            # Start background tasks
            self.subscriber_task = asyncio.create_task(self._message_subscriber())
            self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
            
            logger.info(f"✅ Redis Adapter initialized: {self.server_id}")
            
        except Exception as e:
            logger.error(f"❌ Redis Adapter initialization failed: {e}")
            raise
    
    async def register_handler(self, message_type: MessageType, handler: Callable):
        """Register a message handler"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
        logger.debug(f"📝 Handler registered for {message_type.value}")
    
    async def broadcast_message(self, message: BroadcastMessage) -> bool:
        """Broadcast a message to all servers"""
        try:
            if not self.redis_client:
                logger.error("❌ Redis client not initialized")
                return False
            
            # Set message metadata
            message.sender_server_id = self.server_id
            message.timestamp = datetime.now()
            if not message.message_id:
                message.message_id = f"{self.server_id}-{uuid.uuid4().hex[:8]}"
            
            # Serialize message
            message_data = json.dumps(asdict(message), default=str)
            
            # Determine channel based on scope
            channel = self._get_channel_for_scope(message.scope)
            
            # Publish message
            await self.redis_client.publish(channel, message_data)
            
            # Store message for TTL
            if message.ttl_seconds > 0:
                await self.redis_client.setex(
                    f"message:{message.message_id}",
                    message.ttl_seconds,
                    message_data
                )
            
            self.metrics['messages_sent'] += 1
            logger.debug(f"📡 Message broadcasted: {message.message_type.value} to {channel}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to broadcast message: {e}")
            self.metrics['broadcast_errors'] += 1
            return False
    
    async def broadcast_event_created(
        self, 
        event_data: Dict[str, Any], 
        user_id: int, 
        priority: int = 1
    ) -> bool:
        """Broadcast event created notification"""
        message = BroadcastMessage(
            message_id="",
            message_type=MessageType.EVENT_CREATED,
            scope=BroadcastScope.USER,
            payload={
                'event': event_data,
                'user_id': user_id,
                'priority_level': priority,
                'timestamp': datetime.now().isoformat()
            },
            sender_server_id=self.server_id,
            timestamp=datetime.now(),
            target_users=[user_id],
            priority=priority
        )
        return await self.broadcast_message(message)
    
    async def broadcast_event_updated(
        self, 
        event_data: Dict[str, Any], 
        user_id: int,
        changes: Dict[str, Any] = None
    ) -> bool:
        """Broadcast event updated notification"""
        message = BroadcastMessage(
            message_id="",
            message_type=MessageType.EVENT_UPDATED,
            scope=BroadcastScope.USER,
            payload={
                'event': event_data,
                'user_id': user_id,
                'changes': changes or {},
                'timestamp': datetime.now().isoformat()
            },
            sender_server_id=self.server_id,
            timestamp=datetime.now(),
            target_users=[user_id]
        )
        return await self.broadcast_message(message)
    
    async def broadcast_conflict_detected(
        self, 
        conflict_data: Dict[str, Any], 
        affected_users: List[int]
    ) -> bool:
        """Broadcast schedule conflict detection"""
        message = BroadcastMessage(
            message_id="",
            message_type=MessageType.CONFLICT_DETECTED,
            scope=BroadcastScope.USERS,
            payload={
                'conflict': conflict_data,
                'affected_users': affected_users,
                'severity': conflict_data.get('severity', 'medium'),
                'resolution_suggestions': conflict_data.get('suggestions', []),
                'timestamp': datetime.now().isoformat()
            },
            sender_server_id=self.server_id,
            timestamp=datetime.now(),
            target_users=affected_users,
            priority=1  # High priority for conflicts
        )
        return await self.broadcast_message(message)
    
    async def broadcast_reminder_notification(
        self, 
        reminder_data: Dict[str, Any], 
        user_id: int
    ) -> bool:
        """Broadcast reminder notification"""
        message = BroadcastMessage(
            message_id="",
            message_type=MessageType.REMINDER_NOTIFICATION,
            scope=BroadcastScope.USER,
            payload={
                'reminder': reminder_data,
                'user_id': user_id,
                'notification_time': datetime.now().isoformat()
            },
            sender_server_id=self.server_id,
            timestamp=datetime.now(),
            target_users=[user_id],
            priority=2  # Medium priority for reminders
        )
        return await self.broadcast_message(message)
    
    async def broadcast_priority_alert(
        self, 
        alert_data: Dict[str, Any], 
        user_id: int
    ) -> bool:
        """Broadcast priority alert (CEO meetings, surgery, etc.)"""
        message = BroadcastMessage(
            message_id="",
            message_type=MessageType.PRIORITY_ALERT,
            scope=BroadcastScope.USER,
            payload={
                'alert': alert_data,
                'user_id': user_id,
                'priority_level': alert_data.get('priority', 5),
                'alert_type': alert_data.get('type', 'high_priority_event'),
                'timestamp': datetime.now().isoformat()
            },
            sender_server_id=self.server_id,
            timestamp=datetime.now(),
            target_users=[user_id],
            priority=1  # Always high priority for alerts
        )
        return await self.broadcast_message(message)
    
    async def broadcast_voice_transcription(
        self, 
        transcription_data: Dict[str, Any], 
        user_id: int
    ) -> bool:
        """Broadcast voice transcription result"""
        message = BroadcastMessage(
            message_id="",
            message_type=MessageType.VOICE_TRANSCRIPTION,
            scope=BroadcastScope.USER,
            payload={
                'transcription': transcription_data,
                'user_id': user_id,
                'processing_time': transcription_data.get('processing_time', 0),
                'confidence': transcription_data.get('confidence', 0),
                'timestamp': datetime.now().isoformat()
            },
            sender_server_id=self.server_id,
            timestamp=datetime.now(),
            target_users=[user_id]
        )
        return await self.broadcast_message(message)
    
    async def broadcast_user_presence(
        self, 
        user_id: int, 
        presence_data: Dict[str, Any]
    ) -> bool:
        """Broadcast user presence update"""
        message = BroadcastMessage(
            message_id="",
            message_type=MessageType.USER_PRESENCE,
            scope=BroadcastScope.ALL,
            payload={
                'user_id': user_id,
                'presence': presence_data,
                'timestamp': datetime.now().isoformat()
            },
            sender_server_id=self.server_id,
            timestamp=datetime.now(),
            priority=3  # Low priority for presence
        )
        return await self.broadcast_message(message)
    
    async def broadcast_system_message(
        self, 
        message_text: str, 
        message_data: Dict[str, Any] = None
    ) -> bool:
        """Broadcast system-wide message"""
        message = BroadcastMessage(
            message_id="",
            message_type=MessageType.SYSTEM_BROADCAST,
            scope=BroadcastScope.ALL,
            payload={
                'message': message_text,
                'data': message_data or {},
                'server_id': self.server_id,
                'timestamp': datetime.now().isoformat()
            },
            sender_server_id=self.server_id,
            timestamp=datetime.now(),
            priority=2  # Medium priority for system messages
        )
        return await self.broadcast_message(message)
    
    async def get_server_list(self) -> List[str]:
        """Get list of active servers"""
        try:
            if not self.redis_client:
                return []
            
            # Get servers that have sent heartbeats in the last 2 minutes
            cutoff_time = datetime.now().timestamp() - 120
            servers = []
            
            # Scan for server heartbeats
            async for key in self.redis_client.scan_iter(match="server:*:heartbeat"):
                last_heartbeat = await self.redis_client.get(key)
                if last_heartbeat and float(last_heartbeat) > cutoff_time:
                    server_id = key.split(':')[1]
                    servers.append(server_id)
            
            return servers
            
        except Exception as e:
            logger.error(f"❌ Failed to get server list: {e}")
            return []
    
    async def get_adapter_metrics(self) -> Dict[str, Any]:
        """Get Redis adapter metrics"""
        servers = await self.get_server_list()
        return {
            **self.metrics,
            'active_servers': len(servers),
            'server_list': servers,
            'server_id': self.server_id,
            'redis_connected': self.redis_client is not None
        }
    
    def _get_channel_for_scope(self, scope: BroadcastScope) -> str:
        """Get Redis channel for broadcast scope"""
        if scope == BroadcastScope.ALL:
            return self.broadcast_channel
        elif scope in [BroadcastScope.USER, BroadcastScope.USERS]:
            return self.broadcast_channel
        elif scope == BroadcastScope.ROOM:
            return self.broadcast_channel
        else:
            return self.broadcast_channel
    
    async def _message_subscriber(self):
        """Background task to handle incoming messages"""
        try:
            if not self.pubsub:
                return
            
            logger.info(f"📻 Message subscriber started for {self.server_id}")
            
            async for message in self.pubsub.listen():
                try:
                    if message['type'] != 'message':
                        continue
                    
                    # Parse message
                    message_data = json.loads(message['data'])
                    broadcast_msg = BroadcastMessage(**{
                        **message_data,
                        'timestamp': datetime.fromisoformat(message_data['timestamp']),
                        'message_type': MessageType(message_data['message_type']),
                        'scope': BroadcastScope(message_data['scope'])
                    })
                    
                    # Skip messages from this server
                    if broadcast_msg.sender_server_id == self.server_id:
                        continue
                    
                    # Call handlers
                    handlers = self.message_handlers.get(broadcast_msg.message_type, [])
                    for handler in handlers:
                        try:
                            if asyncio.iscoroutinefunction(handler):
                                await handler(broadcast_msg)
                            else:
                                handler(broadcast_msg)
                        except Exception as e:
                            logger.error(f"❌ Handler error for {broadcast_msg.message_type.value}: {e}")
                    
                    self.metrics['messages_received'] += 1
                    
                except Exception as e:
                    logger.error(f"❌ Message processing error: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Message subscriber error: {e}")
    
    async def _register_server(self):
        """Register this server in Redis"""
        try:
            if not self.redis_client:
                return
            
            # Register server
            await self.redis_client.hset(
                f"server:{self.server_id}:info",
                mapping={
                    'started_at': datetime.now().isoformat(),
                    'last_heartbeat': datetime.now().timestamp(),
                    'status': 'active'
                }
            )
            
            # Set expiry for auto-cleanup
            await self.redis_client.expire(f"server:{self.server_id}:info", 300)
            
            logger.info(f"🏃 Server registered: {self.server_id}")
            
        except Exception as e:
            logger.error(f"❌ Server registration failed: {e}")
    
    async def _heartbeat_loop(self):
        """Background heartbeat task"""
        while True:
            try:
                await asyncio.sleep(30)  # Heartbeat every 30 seconds
                
                if self.redis_client:
                    # Send heartbeat
                    current_time = datetime.now().timestamp()
                    await self.redis_client.setex(
                        f"server:{self.server_id}:heartbeat",
                        120,  # 2 minute expiry
                        current_time
                    )
                    
                    self.metrics['last_heartbeat'] = datetime.now().isoformat()
                    
                    # Update server count
                    servers = await self.get_server_list()
                    self.metrics['servers_discovered'] = len(servers)
                
            except Exception as e:
                logger.error(f"❌ Heartbeat error: {e}")
    
    async def shutdown(self):
        """Shutdown Redis adapter"""
        try:
            # Cancel background tasks
            if self.subscriber_task:
                self.subscriber_task.cancel()
            if self.heartbeat_task:
                self.heartbeat_task.cancel()
            
            # Unregister server
            if self.redis_client:
                await self.redis_client.delete(f"server:{self.server_id}:info")
                await self.redis_client.delete(f"server:{self.server_id}:heartbeat")
            
            # Close connections
            if self.pubsub:
                await self.pubsub.unsubscribe()
                await self.pubsub.close()
            
            if self.redis_client:
                await self.redis_client.close()
            if self.pubsub_client:
                await self.pubsub_client.close()
            
            logger.info(f"🛑 Redis Adapter shutdown: {self.server_id}")
            
        except Exception as e:
            logger.error(f"❌ Shutdown error: {e}")

# Global instance
redis_adapter = RedisAdapter()

async def get_redis_adapter() -> RedisAdapter:
    """Get the global Redis adapter instance"""
    return redis_adapter
