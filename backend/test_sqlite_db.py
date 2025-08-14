#!/usr/bin/env python3
"""
Quick SQLite Database Test Script
Tests CRUD operations independently of the server
"""

import os
import sys
from pathlib import Path
import uuid
from datetime import datetime

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_database_operations():
    """Test basic CRUD operations"""
    print("🧪 Testing SQLite database operations...")
    
    # Set environment
    os.environ['DATABASE_URL'] = 'sqlite:///./kairocal.db'
    
    try:
        # Import models and database
        from app.core.database import get_db, init_engine
        from app.models import User, Event
        
        # Initialize engine
        init_engine()
        db = next(get_db())
        
        print("✅ Database connection established")
        
        # Test 1: Create a user
        print("\n📝 Test 1: Creating user...")
        test_user = User(
            cognito_sub="test-user-sqlite-123",
            email="test-sqlite@example.com",
            full_name="SQLite Test User",
            preferences={"theme": "dark", "timezone": "UTC"}
        )
        
        db.add(test_user)
        db.commit()
        print(f"✅ User created with ID: {test_user.id}")
        
        # Test 2: Query the user
        print("\n🔍 Test 2: Querying user...")
        queried_user = db.query(User).filter(User.email == "test-sqlite@example.com").first()
        if queried_user:
            print(f"✅ User found: {queried_user.full_name}")
            print(f"   Preferences: {queried_user.preferences}")
        else:
            print("❌ User not found")
            return False
        
        # Test 3: Create an event
        print("\n📅 Test 3: Creating event...")
        test_event = Event(
            user_id=test_user.id,
            title="SQLite Test Event",
            description="Testing event creation with SQLite",
            start_time=datetime.now(),
            end_time=datetime.now(),
            priority_level=3,
            priority_confidence=0.95,
            classification_method="bert"
        )
        
        db.add(test_event)
        db.commit()
        print(f"✅ Event created with ID: {test_event.id}")
        
        # Test 4: Query events
        print("\n📋 Test 4: Querying events...")
        user_events = db.query(Event).filter(Event.user_id == test_user.id).all()
        print(f"✅ Found {len(user_events)} events for user")
        
        # Test 5: Update user
        print("\n✏️ Test 5: Updating user...")
        queried_user.preferences = {"theme": "light", "updated": True}
        db.commit()
        
        updated_user = db.query(User).filter(User.id == test_user.id).first()
        print(f"✅ User updated: {updated_user.preferences}")
        
        # Test 6: Clean up
        print("\n🗑️ Test 6: Cleaning up...")
        db.delete(test_event)
        db.delete(test_user)
        db.commit()
        print("✅ Test data cleaned up")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 KairoCal SQLite Database Testing")
    print("=" * 40)
    
    success = test_database_operations()
    
    if success:
        print("\n🎉 SUCCESS: All database operations working!")
        print("💡 SQLite implementation is ready for production")
    else:
        print("\n💥 FAILED: Database operations encountered errors")
        sys.exit(1)
