"""
MCP Server Configuration for KairoCal
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class MCPServerConfig(BaseSettings):
    """Configuration settings for MCP Server"""
    
    # Server Configuration
    mcp_server_name: str = "kairocal-mcp-server"
    mcp_server_version: str = "1.0.0"
    mcp_server_description: str = "Model Context Protocol server for KairoCal AI calendar"
    
    # Connection Settings
    mcp_host: str = "localhost"
    mcp_port: int = 8002
    mcp_transport: str = "stdio"  # stdio, http, or websocket
    
    # Authentication
    mcp_api_key: Optional[str] = None
    
    # Calendar Integration Settings
    calendar_db_url: Optional[str] = None
    enable_voice_commands: bool = True
    enable_bert_integration: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "mcp_server.log"
    
    class Config:
        env_file = ".env"
        env_prefix = "MCP_"

# Global config instance
mcp_config = MCPServerConfig()
