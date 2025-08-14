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

# Check for SQLite mode
sqlite_mode = any(a in ("--sqlite", "--dev-sqlite", "-S") for a in sys.argv[1:])

if sqlite_mode:
    # Set SQLite database URL
    sqlite_db_path = backend_dir / "kairocal.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{sqlite_db_path}"
    print("🗄️  Database Mode: SQLite")
    print(f"📁 Database File: {sqlite_db_path}")
else:
    print("🗄️  Database Mode: PostgreSQL (DATABASE_URL required)")

api_port = int(os.getenv("API_PORT", "8000"))

print("🚀 Starting KairoCal API Server with Enhanced Priority System...")
print(f"📍 Project Root: {project_root}")
print(f"📍 Backend Dir: {backend_dir}")
print(f"📍 Python Path: {sys.path[0]}")
print(f"📍 Server: http://127.0.0.1:{api_port}")
print(f"📖 Docs: http://127.0.0.1:{api_port}/docs")
print(f"🎤 Voice API: http://127.0.0.1:{api_port}/api/v1/voice")
print(f"🧠 Enhanced Priority Classification: ACTIVATED")
print("=" * 70)

if __name__ == "__main__":
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=api_port,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print(f"💡 Make sure you're in the right directory and venv is activated")
        sys.exit(1)
