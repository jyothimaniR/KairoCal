"""
MCP Tools for KairoCal Calendar Operations
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import logging
from mcp.server import Tool
from mcp.types import TextContent

logger = logging.getLogger(__name__)

class CalendarTools:
    """Tools for calendar operations via MCP"""
    
    @staticmethod
    def create_event_tool() -> Tool:
        """Tool for creating calendar events"""
        return Tool(
            name="create_calendar_event",
            description="Create a new calendar event using natural language",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Natural language description of the event"
                    },
                    "suggested_time": {
                        "type": "string",
                        "description": "Suggested time (optional, ISO format)"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Event priority"
                    }
                },
                "required": ["description"]
            }
        )
    
    @staticmethod
    def search_events_tool() -> Tool:
        """Tool for searching calendar events"""
        return Tool(
            name="search_calendar_events",
            description="Search for calendar events using natural language queries",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query in natural language"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date for search (ISO format, optional)"
                    },
                    "end_date": {
                        "type": "string", 
                        "description": "End date for search (ISO format, optional)"
                    }
                },
                "required": ["query"]
            }
        )
    
    @staticmethod
    def detect_conflicts_tool() -> Tool:
        """Tool for detecting calendar conflicts"""
        return Tool(
            name="detect_calendar_conflicts",
            description="Detect potential conflicts in calendar scheduling",
            inputSchema={
                "type": "object",
                "properties": {
                    "proposed_event": {
                        "type": "object",
                        "description": "Proposed event details",
                        "properties": {
                            "title": {"type": "string"},
                            "start_time": {"type": "string"},
                            "end_time": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["title", "start_time", "end_time"]
                    },
                    "check_buffer": {
                        "type": "integer",
                        "description": "Buffer time in minutes to check around the event",
                        "default": 15
                    }
                },
                "required": ["proposed_event"]
            }
        )
    
    @staticmethod
    def voice_command_tool() -> Tool:
        """Tool for processing voice commands"""
        return Tool(
            name="process_voice_command",
            description="Process voice commands for calendar operations",
            inputSchema={
                "type": "object",
                "properties": {
                    "audio_data": {
                        "type": "string",
                        "description": "Base64 encoded audio data or text transcription"
                    },
                    "command_type": {
                        "type": "string",
                        "enum": ["create", "search", "update", "delete", "schedule"],
                        "description": "Type of voice command"
                    }
                },
                "required": ["audio_data"]
            }
        )
    
    @staticmethod
    def get_all_tools() -> List[Tool]:
        """Get all available calendar tools"""
        return [
            CalendarTools.create_event_tool(),
            CalendarTools.search_events_tool(),
            CalendarTools.detect_conflicts_tool(),
            CalendarTools.voice_command_tool()
        ]
