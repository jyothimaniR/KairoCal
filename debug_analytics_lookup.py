#!/usr/bin/env python3
"""
Debug what user the analytics API is actually finding
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session

def debug_user_lookup():
    """Debug what user the get_user_from_cognito function finds"""
    
    print("🔍 Debugging Analytics API User Lookup")
    print("=" * 50)
    
    try:
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        # Try the same lookup as analytics API
        cognito_sub = "frontend-test-user"
        print(f"\n🔍 Looking for user with cognito_sub = '{cognito_sub}'")
        
        user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
        
        if user:
            print(f"✅ Found user:")
            print(f"  ID: {user.id}")
            print(f"  Cognito Sub: {user.cognito_sub}")
            print(f"  Name: {user.full_name}")
            print(f"  Email: {user.email}")
            print(f"  Created: {user.created_at}")
            
            # Check user ID type
            print(f"  ID Type: {type(user.id)}")
            print(f"  ID as String: {str(user.id)}")
            
            # Count events for this user
            from app.models.event import Event
            event_count = db.query(Event).filter(Event.user_id == user.id).count()
            print(f"  Events: {event_count}")
            
        else:
            print("❌ No user found!")
            
        # List all users to compare
        print(f"\n👥 ALL USERS IN DATABASE:")
        all_users = db.query(User).all()
        for u in all_users:
            print(f"  {u.id} | {u.cognito_sub} | {u.full_name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_user_lookup()
