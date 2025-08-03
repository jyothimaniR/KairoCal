"""
WebSocket Server Startup Script for KairoCal
Integrates the ultimate WebSocket server with FastAPI
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.websocket.ultimate_socket_server import UltimateSocketServer
from app.websocket.connection_manager import get_connection_manager
from app.websocket.redis_adapter import get_redis_adapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global WebSocket server instance
socket_server: UltimateSocketServer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global socket_server
    
    try:
        logger.info("🚀 Starting KairoCal WebSocket Server...")
        
        # Initialize WebSocket server
        socket_server = UltimateSocketServer(
            redis_url="redis://localhost:6379",
            secret_key="your-secret-key-change-in-production"
        )
        
        # Initialize all components
        await socket_server.initialize_redis()
        
        logger.info("✅ WebSocket Server startup completed")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    finally:
        # Cleanup on shutdown
        logger.info("🛑 Shutting down WebSocket Server...")
        
        try:
            # Shutdown connection manager
            connection_manager = await get_connection_manager()
            await connection_manager.shutdown()
            
            # Shutdown Redis adapter
            redis_adapter = await get_redis_adapter()
            await redis_adapter.shutdown()
            
            logger.info("✅ WebSocket Server shutdown completed")
            
        except Exception as e:
            logger.error(f"❌ Shutdown error: {e}")

# Create FastAPI app with WebSocket integration
app = FastAPI(
    title="KairoCal WebSocket Server",
    description="Enterprise-grade real-time communication for KairoCal",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO server
@app.on_event("startup")
async def mount_socket_server():
    """Mount Socket.IO server to FastAPI"""
    global socket_server
    if socket_server:
        # Mount the Socket.IO server to the FastAPI app
        app.mount("/socket.io", socket_server.sio.app)
        logger.info("✅ Socket.IO server mounted to FastAPI")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check connection manager
        connection_manager = await get_connection_manager()
        connection_stats = await connection_manager.get_connection_stats()
        
        # Check Redis adapter
        redis_adapter = await get_redis_adapter()
        adapter_metrics = await redis_adapter.get_adapter_metrics()
        
        return {
            "status": "healthy",
            "timestamp": "datetime.now().isoformat()",
            "components": {
                "connection_manager": "healthy" if connection_manager else "error",
                "redis_adapter": "healthy" if redis_adapter else "error",
                "socket_server": "healthy" if socket_server else "error"
            },
            "metrics": {
                "connections": connection_stats,
                "redis": adapter_metrics
            }
        }
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "datetime.now().isoformat()"
        }

# WebSocket stats endpoint
@app.get("/stats")
async def get_websocket_stats():
    """Get WebSocket server statistics"""
    try:
        if not socket_server:
            return {"error": "WebSocket server not initialized"}
        
        # Get connection manager stats
        connection_manager = await get_connection_manager()
        connection_stats = await connection_manager.get_connection_stats()
        
        # Get Redis adapter metrics
        redis_adapter = await get_redis_adapter()
        adapter_metrics = await redis_adapter.get_adapter_metrics()
        
        # Get Socket.IO stats
        socket_stats = {
            "total_sessions": len(socket_server.user_sessions),
            "active_connections": socket_server.connection_metrics.total_connections,
            "active_users": socket_server.connection_metrics.active_users,
            "messages_sent": socket_server.connection_metrics.messages_sent,
            "messages_received": socket_server.connection_metrics.messages_received,
            "errors": socket_server.connection_metrics.errors
        }
        
        return {
            "timestamp": "datetime.now().isoformat()",
            "connection_manager": connection_stats,
            "redis_adapter": adapter_metrics,
            "socket_server": socket_stats
        }
        
    except Exception as e:
        logger.error(f"❌ Stats retrieval failed: {e}")
        return {"error": str(e)}

# Broadcast endpoint for external services
@app.post("/broadcast")
async def broadcast_message(message_data: dict):
    """External API for broadcasting messages"""
    try:
        if not socket_server:
            raise HTTPException(status_code=503, detail="WebSocket server not available")
        
        redis_adapter = await get_redis_adapter()
        
        message_type = message_data.get("type")
        payload = message_data.get("payload", {})
        user_ids = message_data.get("user_ids", [])
        
        if message_type == "event_created":
            success = await redis_adapter.broadcast_event_created(
                payload, user_ids[0] if user_ids else None
            )
        elif message_type == "conflict_detected":
            success = await redis_adapter.broadcast_conflict_detected(payload, user_ids)
        elif message_type == "priority_alert":
            success = await redis_adapter.broadcast_priority_alert(
                payload, user_ids[0] if user_ids else None
            )
        else:
            success = await redis_adapter.broadcast_system_message(
                message_data.get("message", "System notification"),
                payload
            )
        
        return {"success": success, "message_type": message_type}
        
    except Exception as e:
        logger.error(f"❌ Broadcast failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("🌟 Starting KairoCal WebSocket Server...")
    
    # Run with uvicorn
    uvicorn.run(
        "websocket_server:app",
        host="0.0.0.0",
        port=8001,  # Different port from main API
        reload=True,
        log_level="info",
        ws_ping_interval=30,
        ws_ping_timeout=10
    )
