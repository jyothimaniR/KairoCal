@echo off
REM KairoCal MCP Server Installation Script for Windows

echo 🚀 Installing KairoCal MCP Server...

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ Error: Please run this script from the KairoCal root directory
    exit /b 1
)

REM Navigate to backend
cd backend

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements/base.txt

REM Check if MCP dependencies are installed
echo 🔍 Checking MCP dependencies...
python -c "import mcp" 2>nul || pip install mcp

echo ✅ MCP Server installation complete!
echo.
echo 🏃‍♂️ To start the MCP server:
echo    cd backend ^&^& python start_mcp_server.py
echo.
echo 🔧 Configuration file: mcp_config.json
echo 📝 Environment variables: backend/.env
echo.
echo 📖 Available MCP tools:
echo    - create_calendar_event
echo    - search_calendar_events
echo    - detect_calendar_conflicts
echo    - process_voice_command

pause
