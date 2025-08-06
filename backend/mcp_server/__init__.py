"""
KairoCal MCP Server Package
"""

from .server import mcp_server, main
from .config import mcp_config
from .tools import CalendarTools
from .handlers import CalendarHandlers

__version__ = "1.0.0"
__all__ = ["mcp_server", "main", "mcp_config", "CalendarTools", "CalendarHandlers"]
