"""
WebSocket Manager for KairoCal
Handles real-time updates for voice processing, event creation, and priority classification
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class WebSocketMessage:
    """Standard WebSocket message format"""
    type: str
    data: Dict[str, Any]
    timestamp: str
    user_id: Optional[int] = None
    event_id: Optional[int] = None

class ConnectionManager:
    """Manages WebSocket connections and broadcasts"""
    
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # Store all connections for system-wide broadcasts
        self.all_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket, user_id: Optional[int] = None):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        
        # Add to all connections
        self.all_connections.append(websocket)
        
        # Add to user-specific connections if user_id provided
        if user_id:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = []
            self.active_connections[user_id].append(websocket)
            
            logger.info(f"🔌 WebSocket connected for user {user_id}")
            
            # Send welcome message
            await self.send_to_user(user_id, {
                "type": "connection_established",
                "data": {
                    "message": "Connected to KairoCal real-time updates",
                    "user_id": user_id,
                    "features": [
                        "Voice processing updates",
                        "Event creation notifications",
                        "Priority classification results",
                        "System status updates"
                    ]
                }
            })
        else:
            logger.info("🔌 WebSocket connected (anonymous)")

    def disconnect(self, websocket: WebSocket, user_id: Optional[int] = None):
        """Remove a WebSocket connection"""
        # Remove from all connections
        if websocket in self.all_connections:
            self.all_connections.remove(websocket)
        
        # Remove from user-specific connections
        if user_id and user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            
            # Clean up empty user connection lists
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                
            logger.info(f"🔌 WebSocket disconnected for user {user_id}")

    async def send_to_user(self, user_id: int, message: Dict[str, Any]):
        """Send message to all connections for a specific user"""
        if user_id not in self.active_connections:
            logger.warning(f"No active connections for user {user_id}")
            return
        
        # Format message
        ws_message = WebSocketMessage(
            type=message.get("type", "update"),
            data=message.get("data", {}),
            timestamp=datetime.now().isoformat(),
            user_id=user_id
        )
        
        message_json = json.dumps({
            "type": ws_message.type,
            "data": ws_message.data,
            "timestamp": ws_message.timestamp,
            "user_id": ws_message.user_id
        })
        
        # Send to all user connections
        disconnected = []
        for websocket in self.active_connections[user_id]:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.error(f"Error sending to user {user_id}: {e}")
                disconnected.append(websocket)
        
        # Clean up disconnected connections
        for ws in disconnected:
            self.disconnect(ws, user_id)

    async def broadcast_to_all(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        ws_message = WebSocketMessage(
            type=message.get("type", "broadcast"),
            data=message.get("data", {}),
            timestamp=datetime.now().isoformat()
        )
        
        message_json = json.dumps({
            "type": ws_message.type,
            "data": ws_message.data,
            "timestamp": ws_message.timestamp
        })
        
        disconnected = []
        for websocket in self.all_connections:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")
                disconnected.append(websocket)
        
        # Clean up disconnected connections
        for ws in disconnected:
            if ws in self.all_connections:
                self.all_connections.remove(ws)

    async def send_voice_processing_update(self, user_id: int, stage: str, data: Dict[str, Any]):
        """Send voice processing stage updates"""
        await self.send_to_user(user_id, {
            "type": "voice_processing",
            "data": {
                "stage": stage,
                "message": self._get_stage_message(stage),
                "progress": self._get_stage_progress(stage),
                "details": data
            }
        })

    async def send_priority_classification_update(self, user_id: int, voice_text: str, 
                                                nlp_priority: int, bert_priority: int, 
                                                final_priority: int, confidence: float):
        """Send priority classification results"""
        await self.send_to_user(user_id, {
            "type": "priority_classification",
            "data": {
                "voice_text": voice_text,
                "nlp_priority": nlp_priority,
                "bert_priority": bert_priority,
                "final_priority": final_priority,
                "confidence": confidence,
                "priority_label": self._get_priority_label(final_priority),
                "classification_method": "hybrid_ai_rules"
            }
        })

    async def send_event_creation_update(self, user_id: int, event_data: Dict[str, Any], 
                                       success: bool, event_id: Optional[int] = None):
        """Send event creation results"""
        await self.send_to_user(user_id, {
            "type": "event_created",
            "data": {
                "success": success,
                "event_id": event_id,
                "event_data": event_data,
                "message": "✅ Event created successfully!" if success else "❌ Event creation failed"
            }
        })

    async def send_system_status_update(self, status: str, details: Dict[str, Any]):
        """Send system-wide status updates"""
        await self.broadcast_to_all({
            "type": "system_status",
            "data": {
                "status": status,
                "details": details,
                "services": {
                    "voice_api": "operational",
                    "bert_model": "trained",
                    "priority_classification": "enhanced",
                    "database": "connected"
                }
            }
        })

    def _get_stage_message(self, stage: str) -> str:
        """Get user-friendly message for processing stage"""
        messages = {
            "voice_received": "🎤 Voice input received",
            "voice_cleaning": "🧹 Cleaning voice text",
            "nlp_processing": "🔍 Analyzing with enhanced NLP",
            "bert_classification": "🤖 BERT AI classification",
            "hybrid_decision": "⚖️ Making hybrid priority decision",
            "event_creation": "📅 Creating calendar event",
            "completed": "✅ Processing completed"
        }
        return messages.get(stage, f"Processing: {stage}")

    def _get_stage_progress(self, stage: str) -> int:
        """Get progress percentage for processing stage"""
        progress = {
            "voice_received": 10,
            "voice_cleaning": 25,
            "nlp_processing": 45,
            "bert_classification": 65,
            "hybrid_decision": 80,
            "event_creation": 95,
            "completed": 100
        }
        return progress.get(stage, 0)

    def _get_priority_label(self, priority: int) -> str:
        """Get human-readable priority label"""
        labels = {
            1: "Very Low",
            2: "Low", 
            3: "Normal",
            4: "High",
            5: "Critical"
        }
        return labels.get(priority, "Unknown")

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get WebSocket connection statistics"""
        return {
            "total_connections": len(self.all_connections),
            "user_connections": len(self.active_connections),
            "users_online": list(self.active_connections.keys())
        }

# Global connection manager instance
manager = ConnectionManager()
