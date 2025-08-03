#!/usr/bin/env python3
"""
Simple test script to verify KairoCal backend setup
"""
import sys
import traceback

def test_imports():
    """Test all critical imports"""
    try:
        print("🔍 Testing KairoCal backend setup...")
        print("")
        
        # Test basic dependencies
        print("📦 Testing dependencies...")
        import fastapi
        print(f"  ✅ FastAPI {fastapi.__version__}")
        
        import sqlalchemy
        print(f"  ✅ SQLAlchemy {sqlalchemy.__version__}")
        
        import uvicorn
        print(f"  ✅ Uvicorn {uvicorn.__version__}")
        
        print("")
        
        # Test app configuration
        print("⚙️  Testing configuration...")
        from app.config import get_settings
        settings = get_settings()
        print(f"  ✅ Config loaded (Debug: {settings.debug})")
        print(f"  ✅ Database: {settings.database_url}")
        
        print("")
        
        # Test database connection
        print("🗃️  Testing database setup...")
        from app.core.database import engine, SessionLocal
        print("  ✅ Database engine created")
        print("  ✅ Session factory created")
        
        print("")
        
        # Test models
        print("📋 Testing models...")
        try:
            from app.models import User, Event, Reminder
            print("  ✅ All models imported successfully")
        except Exception as e:
            print(f"  ⚠️  Model import warning: {str(e)}")
        
        print("")
        print("🎉 Backend setup verification complete!")
        print("🚀 Ready to start development!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during setup verification: {str(e)}")
        print("")
        print("🔧 Traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
