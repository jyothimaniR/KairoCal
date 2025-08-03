# scripts/simple_demo_data.py
"""
Generate simplified demo data for analytics testing
"""

import json
import random
from datetime import datetime, timedelta
import uuid

def generate_simple_demo_data():
    """Generate demo data SQL that matches the actual table structure"""
    
    # Create 3 demo users
    users = [
        {
            "id": str(uuid.uuid4()),
            "cognito_sub": "demo_user_001",
            "email": "sarah.chen@company.com", 
            "name": "Sarah Chen"
        },
        {
            "id": str(uuid.uuid4()),
            "cognito_sub": "demo_user_002", 
            "email": "marcus.rodriguez@company.com",
            "name": "Marcus Rodriguez"
        },
        {
            "id": str(uuid.uuid4()),
            "cognito_sub": "demo_user_003",
            "email": "emily.watson@company.com",
            "name": "Emily Watson"
        }
    ]
    
    # Generate SQL for users
    users_sql = []
    for user in users:
        users_sql.append(f"""
INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
VALUES ('{user["id"]}', '{user["cognito_sub"]}', '{user["email"]}', '{user["name"]}', 
        '{{"demo": true}}', true, now(), now())
ON CONFLICT (cognito_sub) DO UPDATE SET 
    email = EXCLUDED.email, full_name = EXCLUDED.full_name, updated_at = now();
""")
    
    # Generate events for each user
    events_sql = []
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(weeks=8)
    
    meeting_types = ["Team Meeting", "1:1 Check-in", "Project Review", "Client Call", "Planning Session", "All Hands", "Training", "Brainstorm"]
    outcomes = ["productive", "neutral", "waste"]
    created_via_options = ["manual", "voice", "imported", "text"]
    
    for user in users:
        # Generate 8-12 events per week for 8 weeks
        for week in range(8):
            events_this_week = random.randint(8, 12)
            
            for event_num in range(events_this_week):
                # Random weekday (skip most weekends)
                week_start = start_date + timedelta(weeks=week)
                weekday = random.randint(0, 4)  # Mon-Fri
                if random.random() < 0.1:  # 10% chance of weekend
                    weekday = random.randint(5, 6)
                
                event_date = week_start + timedelta(days=weekday)
                
                # Random time between 8 AM and 6 PM
                hour = random.randint(8, 17)
                minute = random.choice([0, 15, 30, 45])
                start_time = event_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # Duration 30-120 minutes
                duration = random.choice([30, 45, 60, 90, 120])
                end_time = start_time + timedelta(minutes=duration)
                planned_duration = duration + random.randint(-15, 15)
                actual_duration = duration + random.randint(-10, 20)
                
                # Analytics fields
                effectiveness = random.randint(1, 5)
                energy = random.randint(1, 5)
                outcome = random.choice(outcomes)
                created_via = random.choice(created_via_options)
                
                event_id = str(uuid.uuid4())
                title = random.choice(meeting_types)
                
                events_sql.append(f"""
INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '{event_id}', '{user["id"]}', '{title}', 'Demo analytics data',
    '{start_time.isoformat()}', '{end_time.isoformat()}', 'Conference Room',
    false, null, '{outcome}', {effectiveness}, {energy}, '{created_via}',
    {actual_duration}, {planned_duration}, '{start_time.isoformat()}', '{start_time.isoformat()}'
);""")
    
    return users_sql, events_sql

def write_simple_sql_file():
    """Write SQL to file"""
    users_sql, events_sql = generate_simple_demo_data()
    
    # Write to file
    with open('simple_demo_data.sql', 'w') as f:
        f.write("-- Simple Analytics Demo Data\n")
        f.write("-- Users\n")
        f.write("\n".join(users_sql))
        f.write("\n\n-- Events\n")  
        f.write("\n".join(events_sql))
    
    print(f"✅ Generated simple_demo_data.sql with {len(users_sql)} users and {len(events_sql)} events")

if __name__ == "__main__":
    write_simple_sql_file()
