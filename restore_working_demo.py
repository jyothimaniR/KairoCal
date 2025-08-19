#!/usr/bin/env python3
"""
Restore the working demo data that was functioning perfectly
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
import json

def restore_demo_data():
    """Restore the exact demo data that was working perfectly"""
    
    # Connect to database
    conn = sqlite3.connect('kairocal.db')
    cursor = conn.cursor()
    
    print("🎭 Restoring working demo data...")
    
    # Create demo user (same as before)
    demo_user_id = str(uuid.uuid4())
    demo_cognito_sub = "demo-user-presentation"
    
    # Insert demo user
    cursor.execute("""
        INSERT INTO users (
            id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        demo_user_id,
        demo_cognito_sub,
        "demo@kairocal.com",
        "Demo User",
        json.dumps({
            "default_event_duration": "smart",
            "timezone": "UTC",
            "notifications_enabled": True,
            "voice_commands_enabled": True
        }),
        True,
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))
    
    print(f"✅ Created demo user: {demo_cognito_sub}")
    
    # Create realistic demo events with ALL required fields
    base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    demo_events = [
        # Today's events (completed)
        {
            "title": "Team Standup Meeting",
            "description": "Daily team sync and progress update",
            "start": base_date,
            "duration": 30,
            "priority": 3,
            "location": "Conference Room A",
            "created_via": "voice",
            "classification_method": "bert",
            "priority_confidence": 0.85,
            "meeting_outcome": "completed",
            "effectiveness_rating": 4,
            "energy_level": 4
        },
        {
            "title": "Product Strategy Review",
            "description": "Quarterly product roadmap discussion with leadership team",
            "start": base_date + timedelta(hours=2),
            "duration": 90,
            "priority": 1,
            "location": "Executive Boardroom",
            "created_via": "manual",
            "classification_method": "bert",
            "priority_confidence": 0.92,
            "meeting_outcome": "completed",
            "effectiveness_rating": 5,
            "energy_level": 5
        },
        {
            "title": "Client Demo Preparation",
            "description": "Final rehearsal for tomorrow's client presentation",
            "start": base_date + timedelta(hours=4),
            "duration": 60,
            "priority": 2,
            "location": "Demo Room",
            "created_via": "voice",
            "classification_method": "bert",
            "priority_confidence": 0.78,
            "meeting_outcome": "completed",
            "effectiveness_rating": 4,
            "energy_level": 3
        },
        {
            "title": "Doctor Appointment",
            "description": "Annual health checkup",
            "start": base_date + timedelta(hours=6),
            "duration": 45,
            "priority": 2,
            "location": "Medical Center",
            "created_via": "voice",
            "classification_method": "bert",
            "priority_confidence": 0.89,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,  # Default for pending
            "energy_level": 3           # Default for pending
        },
        
        # Tomorrow's events
        {
            "title": "CEO Board Meeting",
            "description": "Monthly board review and strategic planning session",
            "start": base_date + timedelta(days=1, hours=1),
            "duration": 120,
            "priority": 1,
            "location": "Executive Boardroom",
            "created_via": "manual",
            "classification_method": "bert",
            "priority_confidence": 0.95,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,
            "energy_level": 3
        },
        {
            "title": "Client Presentation - KairoCal Demo",
            "description": "Live demonstration of AI-powered scheduling capabilities",
            "start": base_date + timedelta(days=1, hours=3),
            "duration": 75,
            "priority": 1,
            "location": "Client Office",
            "created_via": "voice",
            "classification_method": "bert",
            "priority_confidence": 0.91,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,
            "energy_level": 3
        },
        {
            "title": "Team Lunch",
            "description": "Celebration lunch for successful product launch",
            "start": base_date + timedelta(days=1, hours=5),
            "duration": 90,
            "priority": 4,
            "location": "The Garden Restaurant",
            "created_via": "manual",
            "classification_method": "bert",
            "priority_confidence": 0.65,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,
            "energy_level": 3
        },
        
        # This week's events
        {
            "title": "Sprint Planning",
            "description": "Agile sprint planning for Q4 features",
            "start": base_date + timedelta(days=2, hours=2),
            "duration": 120,
            "priority": 2,
            "location": "Development Center",
            "created_via": "voice",
            "classification_method": "bert",
            "priority_confidence": 0.82,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,
            "energy_level": 3
        },
        {
            "title": "Technical Architecture Review",
            "description": "Deep dive into AI model optimization and scaling",
            "start": base_date + timedelta(days=2, hours=5),
            "duration": 90,
            "priority": 2,
            "location": "Tech Lab",
            "created_via": "manual",
            "classification_method": "bert",
            "priority_confidence": 0.87,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,
            "energy_level": 3
        },
        {
            "title": "Investor Call",
            "description": "Quarterly investor update and funding discussion",
            "start": base_date + timedelta(days=3, hours=2),
            "duration": 60,
            "priority": 1,
            "location": "Conference Call",
            "created_via": "voice",
            "classification_method": "bert",
            "priority_confidence": 0.93,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,
            "energy_level": 3
        },
        {
            "title": "Marketing Campaign Review",
            "description": "Q4 marketing strategy and budget allocation",
            "start": base_date + timedelta(days=4, hours=3),
            "duration": 75,
            "priority": 3,
            "location": "Marketing Hub",
            "created_via": "manual",
            "classification_method": "bert",
            "priority_confidence": 0.76,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,
            "energy_level": 3
        },
        {
            "title": "Code Review Session",
            "description": "Review BERT integration and voice processing improvements",
            "start": base_date + timedelta(days=4, hours=6),
            "duration": 90,
            "priority": 3,
            "location": "Development Center",
            "created_via": "voice",
            "classification_method": "bert",
            "priority_confidence": 0.81,
            "meeting_outcome": "pending",
            "effectiveness_rating": 3,
            "energy_level": 3
        }
    ]
    
    # Insert events with all required fields
    for event in demo_events:
        event_id = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO events (
                id, user_id, title, description, start_time, end_time, is_all_day,
                location, priority_level, priority_confidence, classification_method,
                meeting_outcome, effectiveness_rating, energy_level, created_via,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id,
            demo_user_id,
            event["title"],
            event["description"],
            event["start"].isoformat(),
            (event["start"] + timedelta(minutes=event["duration"])).isoformat(),
            False,
            event["location"],
            event["priority"],
            event["priority_confidence"],
            event["classification_method"],
            event["meeting_outcome"],
            event["effectiveness_rating"],
            event["energy_level"],
            event["created_via"],
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
    
    print(f"✅ Created {len(demo_events)} demo events")
    
    # Create some intentional conflicts for conflict detection demo
    conflict_events = [
        {
            "title": "Emergency Client Call",
            "description": "Urgent customer escalation requiring immediate attention",
            "start": base_date + timedelta(days=1, hours=3, minutes=30),  # Overlaps with client demo
            "duration": 60,
            "priority": 1,
            "location": "Conference Call",
            "created_via": "voice",
            "classification_method": "bert",
            "priority_confidence": 0.88
        },
        {
            "title": "Team Building Event",
            "description": "Optional team bonding activity",
            "start": base_date + timedelta(days=1, hours=4, minutes=45),  # Overlaps with client demo
            "duration": 90,
            "priority": 5,
            "location": "Recreation Area",
            "created_via": "manual",
            "classification_method": "bert",
            "priority_confidence": 0.45
        }
    ]
    
    for event in conflict_events:
        event_id = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO events (
                id, user_id, title, description, start_time, end_time, is_all_day,
                location, priority_level, priority_confidence, classification_method,
                meeting_outcome, effectiveness_rating, energy_level, created_via,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id,
            demo_user_id,
            event["title"],
            event["description"],
            event["start"].isoformat(),
            (event["start"] + timedelta(minutes=event["duration"])).isoformat(),
            False,
            event["location"],
            event["priority"],
            event["priority_confidence"],
            event["classification_method"],
            "pending",
            3,  # Default effectiveness rating
            3,  # Default energy level
            event["created_via"],
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
    
    print(f"✅ Created {len(conflict_events)} conflict events for demonstration")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"""
🎭 WORKING DEMO DATA RESTORED!

📊 Demo Account Details:
   - User ID: {demo_user_id}
   - Cognito Sub: {demo_cognito_sub}
   - Email: demo@kairocal.com
   - Total Events: {len(demo_events) + len(conflict_events)}

🎯 Demo Features Working:
   ✅ All required fields populated
   ✅ Diverse event types and priorities
   ✅ Voice and manual event creation
   ✅ BERT classification with confidence
   ✅ Completed and pending events
   ✅ Effectiveness ratings and energy levels
   ✅ Intentional conflicts for demo
   ✅ Analytics will show real productivity data

🚀 Ready for your demo - all features should work perfectly!
""")

if __name__ == "__main__":
    restore_demo_data()
