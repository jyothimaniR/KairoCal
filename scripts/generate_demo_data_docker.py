# scripts/generate_demo_data_docker.py
"""
Generate analytics demo data using Docker exec commands
"""

import json
import random
from datetime import datetime, timedelta
import uuid

def generate_demo_data():
    """Generate demo data SQL and execute via Docker"""
    
    # User profiles
    users = [
        {
            "id": str(uuid.uuid4()),
            "cognito_sub": "demo_user_001",
            "email": "sarah.chen@company.com", 
            "name": "Sarah Chen",
            "pattern": "high_performer"
        },
        {
            "id": str(uuid.uuid4()),
            "cognito_sub": "demo_user_002",
            "email": "marcus.rodriguez@company.com",
            "name": "Marcus Rodriguez", 
            "pattern": "morning_person"
        },
        {
            "id": str(uuid.uuid4()),
            "cognito_sub": "demo_user_003",
            "email": "emily.watson@company.com",
            "name": "Emily Watson",
            "pattern": "afternoon_focus"
        }
    ]
    
    # Generate users SQL
    users_sql = []
    for user in users:
        users_sql.append(f"""
INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
VALUES ('{user["id"]}', '{user["cognito_sub"]}', '{user["email"]}', '{user["name"]}', 
        '{{"pattern": "{user["pattern"]}"}}', true, now(), now())
ON CONFLICT (cognito_sub) DO UPDATE SET 
    email = EXCLUDED.email, full_name = EXCLUDED.full_name, updated_at = now();
""")
    
    # Generate events for each user
    events_sql = []
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(weeks=8)
    
    meeting_types = ["Team Meeting", "1:1 Check-in", "Project Review", "Client Call", "Planning Session"]
    outcomes = ["productive", "neutral", "waste"]
    created_via = ["manual", "voice", "imported", "text"]
    
    for user in users:
        # Generate 10-15 events per week for 8 weeks
        for week in range(8):
            events_this_week = random.randint(10, 15)
            
            for event_num in range(events_this_week):
                # Random day in the week
                week_start = start_date + timedelta(weeks=week)
                random_day = random.randint(0, 6)
                event_date = week_start + timedelta(days=random_day)
                
                # Skip weekends mostly
                if event_date.weekday() >= 5 and random.random() > 0.2:
                    continue
                
                # Random time between 8 AM and 6 PM
                hour = random.randint(8, 17)
                minute = random.choice([0, 15, 30, 45])
                start_time = event_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # Duration 30-120 minutes
                duration = random.choice([30, 45, 60, 90, 120])
                end_time = start_time + timedelta(minutes=duration)
                planned_duration = duration + random.randint(-15, 15)
                actual_duration = duration + random.randint(-10, 20)
                
                # Analytics fields based on time and pattern
                if user["pattern"] == "high_performer":
                    effectiveness = random.choices([3, 4, 5], weights=[0.2, 0.4, 0.4])[0]
                    energy = random.choices([3, 4, 5], weights=[0.3, 0.4, 0.3])[0]
                elif user["pattern"] == "morning_person":
                    if hour <= 12:
                        effectiveness = random.choices([4, 5], weights=[0.5, 0.5])[0]
                        energy = random.choices([4, 5], weights=[0.6, 0.4])[0]
                    else:
                        effectiveness = random.choices([2, 3, 4], weights=[0.3, 0.5, 0.2])[0]
                        energy = random.choices([2, 3, 4], weights=[0.4, 0.4, 0.2])[0]
                else:  # afternoon_focus
                    if hour >= 13:
                        effectiveness = random.choices([4, 5], weights=[0.6, 0.4])[0]
                        energy = random.choices([3, 4, 5], weights=[0.3, 0.4, 0.3])[0]
                    else:
                        effectiveness = random.choices([2, 3], weights=[0.4, 0.6])[0]
                        energy = random.choices([2, 3], weights=[0.5, 0.5])[0]
                
                # Meeting outcome based on effectiveness
                if effectiveness >= 4:
                    outcome = random.choices(outcomes, weights=[0.7, 0.2, 0.1])[0]
                elif effectiveness <= 2:
                    outcome = random.choices(outcomes, weights=[0.2, 0.3, 0.5])[0]
                else:
                    outcome = random.choices(outcomes, weights=[0.4, 0.5, 0.1])[0]
                
                event_id = str(uuid.uuid4())
                title = random.choice(meeting_types)
                priority = random.randint(1, 5)
                confidence = random.uniform(0.6, 0.95)
                method = random.choice(["manual", "bert", "rule_based"])
                creation = random.choice(created_via)
                
                events_sql.append(f"""
INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '{event_id}', '{user["id"]}', '{title}', 'Demo analytics data',
    '{start_time.isoformat()}', '{end_time.isoformat()}', 'Conference Room',
    false, null, {priority}, {confidence:.3f}, '{method}',
    '{outcome}', {effectiveness}, {energy}, '{creation}',
    {actual_duration}, {planned_duration}, '{start_time.isoformat()}', '{start_time.isoformat()}'
);""")
    
    return users_sql, events_sql

def write_sql_file():
    """Write SQL to file and execute"""
    users_sql, events_sql = generate_demo_data()
    
    # Write to file
    with open('demo_data.sql', 'w') as f:
        f.write("-- Analytics Demo Data\n")
        f.write("-- Users\n")
        f.write("\n".join(users_sql))
        f.write("\n\n-- Events\n")
        f.write("\n".join(events_sql))
    
    print(f"✅ Generated demo_data.sql with {len(users_sql)} users and {len(events_sql)} events")

if __name__ == "__main__":
    write_sql_file()
