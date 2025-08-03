#!/usr/bin/env python3
"""
Simple server starter for KairoCal API with enhanced priority system
"""
import os
import sys
import uvicorn

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set working directory
os.chdir(current_dir)

print("🚀 Starting KairoCal API Server with Enhanced Priority System...")
print("📍 Server: http://127.0.0.1:8001")
print("📖 Docs: http://127.0.0.1:8001/docs")
print("🎤 Voice API: http://127.0.0.1:8001/api/v1/voice")
print("🧠 Enhanced Priority Classification: ACTIVATED")
print("=" * 60)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=False,
        log_level="info"
    )
