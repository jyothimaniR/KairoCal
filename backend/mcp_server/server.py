"""
KairoCal MCP Server Implementation
"""

import asyncio
import logging
import json
from typing import Any, Dict, List
from datetime import datetime

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from .config import mcp_config
from .tools import CalendarTools
from .handlers import CalendarHandlers

# Configure logging
logging.basicConfig(
    level=getattr(logging, mcp_config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(mcp_config.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class KairoCalMCPServer:
    """Main MCP Server for KairoCal"""
    
    def __init__(self):
        self.server = Server(mcp_config.mcp_server_name)
        self.handlers = CalendarHandlers()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP server handlers"""
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available resources"""
            return [
                Resource(
                    uri="calendar://events",
                    name="Calendar Events",
                    description="Access to calendar events data",
                    mimeType="application/json"
                ),
                Resource(
                    uri="calendar://conflicts",
                    name="Conflict Detection",
                    description="Calendar conflict detection service",
                    mimeType="application/json"
                ),
                Resource(
                    uri="calendar://voice-commands",
                    name="Voice Commands",
                    description="Voice command processing for calendar",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read resource content"""
            if uri == "calendar://events":
                events = await self.handlers.get_recent_events()
                return json.dumps(events, default=str)
            elif uri == "calendar://conflicts":
                conflicts = await self.handlers.get_recent_conflicts()
                return json.dumps(conflicts, default=str)
            elif uri == "calendar://voice-commands":
                commands = await self.handlers.get_voice_command_history()
                return json.dumps(commands, default=str)
            else:
                raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools"""
            return CalendarTools.get_all_tools()
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute tool calls"""
            try:
                logger.info(f"Executing tool: {name} with arguments: {arguments}")
                
                if name == "create_calendar_event":
                    result = await self.handlers.create_event(arguments)
                elif name == "search_calendar_events":
                    result = await self.handlers.search_events(arguments)
                elif name == "detect_calendar_conflicts":
                    result = await self.handlers.detect_conflicts(arguments)
                elif name == "process_voice_command":
                    result = await self.handlers.process_voice_command(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, default=str, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error executing tool {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
    
    async def run_stdio(self):
        """Run server with stdio transport"""
        logger.info(f"Starting {mcp_config.mcp_server_name} with stdio transport")
        await self.server.run_stdio()
    
    async def run_http(self):
        """Run server with HTTP transport"""
        logger.info(f"Starting {mcp_config.mcp_server_name} on {mcp_config.mcp_host}:{mcp_config.mcp_port}")
        await self.server.run_http(
            host=mcp_config.mcp_host,
            port=mcp_config.mcp_port
        )

# Server instance
mcp_server = KairoCalMCPServer()

async def main():
    """Main entry point"""
    if mcp_config.mcp_transport == "stdio":
        await mcp_server.run_stdio()
    elif mcp_config.mcp_transport == "http":
        await mcp_server.run_http()
    else:
        raise ValueError(f"Unsupported transport: {mcp_config.mcp_transport}")

if __name__ == "__main__":
    asyncio.run(main())
