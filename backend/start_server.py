#!/usr/bin/env python3
"""
KairoCal Backend Server - Production Ready Starter
"""
import os
import sys
import uvicorn
from pathlib import Path

# Ensure we're in the right directory and Python path is set
project_root = Path(__file__).parent.parent
backend_dir = Path(__file__).parent
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

print("🚀 Starting KairoCal API Server with Enhanced Priority System...")
print(f"📍 Project Root: {project_root}")
print(f"📍 Backend Dir: {backend_dir}")
print(f"📍 Python Path: {sys.path[0]}")
print(f"📍 Server: http://127.0.0.1:8001")
print(f"📖 Docs: http://127.0.0.1:8001/docs")
print(f"🎤 Voice API: http://127.0.0.1:8001/api/v1/voice")
print(f"🧠 Enhanced Priority Classification: ACTIVATED")
print("=" * 70)

if __name__ == "__main__":
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8001,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print(f"💡 Make sure you're in the right directory and venv is activated")
        sys.exit(1)
