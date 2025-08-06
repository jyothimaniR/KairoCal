#!/bin/bash
# KairoCal MCP Server Installation Script

echo "🚀 Installing KairoCal MCP Server..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the KairoCal root directory"
    exit 1
fi

# Navigate to backend
cd backend

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements/base.txt

# Check if MCP dependencies are installed
echo "🔍 Checking MCP dependencies..."
python -c "import mcp" 2>/dev/null || pip install mcp

# Make startup script executable
chmod +x start_mcp_server.py

echo "✅ MCP Server installation complete!"
echo ""
echo "🏃‍♂️ To start the MCP server:"
echo "   cd backend && python start_mcp_server.py"
echo ""
echo "🔧 Configuration file: mcp_config.json"
echo "📝 Environment variables: backend/.env"
echo ""
echo "📖 Available MCP tools:"
echo "   - create_calendar_event"
echo "   - search_calendar_events" 
echo "   - detect_calendar_conflicts"
echo "   - process_voice_command"
