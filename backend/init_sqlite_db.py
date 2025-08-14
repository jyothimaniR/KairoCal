#!/usr/bin/env python3
"""
SQLite Database Initialization Script
Creates all tables for KairoCal using SQLAlchemy models
"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def init_sqlite_database():
    """Initialize SQLite database with all tables"""
    print("🗄️  Initializing SQLite database...")
    
    # Set environment for SQLite
    os.environ['DATABASE_URL'] = 'sqlite:///./kairocal.db'
    
    try:
        # Import after setting environment
        from app.core.database import Base, init_engine, get_db
        from app.models import User, Event, Reminder
        
        print("📦 Models imported successfully")
        
        # Initialize engine
        engine = init_engine()
        print("🔧 Database engine initialized")
        
        # Create all tables
        print("🏗️  Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database initialization complete!")
        print(f"📁 Database file: {os.path.abspath('kairocal.db')}")
        
        # Test connection
        print("🔍 Testing database connection...")
        db = next(get_db())
        
        # Simple query test
        from sqlalchemy import text
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        
        print(f"📋 Tables created: {', '.join(tables)}")
        db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 KairoCal SQLite Database Setup")
    print("=" * 40)
    
    success = init_sqlite_database()
    
    if success:
        print("\n🎉 SUCCESS: Database is ready!")
        print("💡 You can now start the backend server:")
        print("   python start_server.py")
    else:
        print("\n💥 FAILED: Database setup encountered errors")
        sys.exit(1)
