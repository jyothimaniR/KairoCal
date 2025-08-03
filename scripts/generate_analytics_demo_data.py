# scripts/generate_analytics_demo_data.py
"""
Generate 8 weeks of realistic analytics demo data for KairoCal Analytics Dashboard

This script creates comprehensive demo data including:
- Users with varied productivity patterns
- Events with analytics fields (effectiveness_rating, energy_level, meeting_outcome, etc.)
- Realistic scheduling patterns and productivity trends
- ML-ready data for analytics engine testing
"""

import random
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor

# Add the backend app directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.database import get_db
from app.models.user import User
from app.models.event import Event


class AnalyticsDemoDataGenerator:
    """Generate realistic analytics demo data for 8 weeks"""
    
    def __init__(self):
        # Database connection details from docker-compose
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'kairocal',
            'user': 'kairocal_user',
            'password': 'Test123'
        }
        
        # Demo user profiles with different productivity patterns
        self.user_profiles = [
            {
                "name": "Sarah Chen",
                "email": "sarah.chen@company.com", 
                "cognito_sub": "demo_user_001",
                "pattern": "high_performer",  # Consistently high productivity
                "preferences": {
                    "peak_hours": [9, 10, 11, 14, 15],
                    "low_energy": [16, 17, 18],
                    "preferred_days": [1, 2, 3, 4],  # Mon-Thu
                    "meeting_types": ["strategic", "one_on_one", "planning"],
                    "avg_effectiveness": 4.2,
                    "energy_consistency": 0.8
                }
            },
            {
                "name": "Marcus Rodriguez", 
                "email": "marcus.rodriguez@company.com",
                "cognito_sub": "demo_user_002", 
                "pattern": "morning_person",  # High productivity in mornings
                "preferences": {
                    "peak_hours": [8, 9, 10, 11],
                    "low_energy": [14, 15, 16, 17],
                    "preferred_days": [0, 1, 2, 4],  # Mon, Tue, Wed, Fri
                    "meeting_types": ["team_standup", "review", "planning"],
                    "avg_effectiveness": 3.8,
                    "energy_consistency": 0.9
                }
            },
            {
                "name": "Emily Watson",
                "email": "emily.watson@company.com", 
                "cognito_sub": "demo_user_003",
                "pattern": "afternoon_focus",  # Better productivity after lunch
                "preferences": {
                    "peak_hours": [13, 14, 15, 16],
                    "low_energy": [8, 9, 17, 18],
                    "preferred_days": [1, 2, 3, 4, 5],  # Mon-Fri
                    "meeting_types": ["client_call", "presentation", "brainstorm"],
                    "avg_effectiveness": 3.6,
                    "energy_consistency": 0.6
                }
            },
            {
                "name": "David Kim",
                "email": "david.kim@company.com",
                "cognito_sub": "demo_user_004", 
                "pattern": "inconsistent",  # Variable productivity patterns
                "preferences": {
                    "peak_hours": [10, 11, 14, 15, 16],
                    "low_energy": [12, 13, 17, 18],
                    "preferred_days": [0, 1, 2, 3, 4],  # Mon-Fri
                    "meeting_types": ["all_hands", "training", "social"],
                    "avg_effectiveness": 3.1,
                    "energy_consistency": 0.4
                }
            },
            {
                "name": "Lisa Thompson",
                "email": "lisa.thompson@company.com",
                "cognito_sub": "demo_user_005",
                "pattern": "improver",  # Productivity improving over time
                "preferences": {
                    "peak_hours": [9, 10, 11, 15, 16],
                    "low_energy": [12, 13, 17],
                    "preferred_days": [1, 2, 3, 4],  # Tue-Fri
                    "meeting_types": ["project_sync", "mentoring", "feedback"],
                    "avg_effectiveness": 3.4,  # Will improve over time
                    "energy_consistency": 0.7
                }
            }
        ]
        
        # Meeting types with different characteristics
        self.meeting_types = {
            "team_standup": {
                "duration_range": (15, 30),
                "effectiveness_bias": 0.2,  # Usually effective
                "energy_impact": -0.1,
                "outcome_weights": {"productive": 0.7, "neutral": 0.2, "waste": 0.1}
            },
            "one_on_one": {
                "duration_range": (30, 60), 
                "effectiveness_bias": 0.3,
                "energy_impact": 0.1,
                "outcome_weights": {"productive": 0.8, "neutral": 0.15, "waste": 0.05}
            },
            "strategic": {
                "duration_range": (60, 120),
                "effectiveness_bias": 0.1,
                "energy_impact": -0.2,
                "outcome_weights": {"productive": 0.6, "neutral": 0.3, "waste": 0.1}
            },
            "client_call": {
                "duration_range": (30, 90),
                "effectiveness_bias": 0.0,
                "energy_impact": -0.1,
                "outcome_weights": {"productive": 0.5, "neutral": 0.4, "waste": 0.1}
            },
            "all_hands": {
                "duration_range": (45, 90),
                "effectiveness_bias": -0.2,
                "energy_impact": -0.3,
                "outcome_weights": {"productive": 0.3, "neutral": 0.4, "waste": 0.3}
            },
            "training": {
                "duration_range": (60, 180),
                "effectiveness_bias": 0.1,
                "energy_impact": -0.1,
                "outcome_weights": {"productive": 0.6, "neutral": 0.3, "waste": 0.1}
            },
            "brainstorm": {
                "duration_range": (45, 90),
                "effectiveness_bias": 0.0,
                "energy_impact": 0.1,
                "outcome_weights": {"productive": 0.5, "neutral": 0.3, "waste": 0.2}
            },
            "review": {
                "duration_range": (30, 60),
                "effectiveness_bias": 0.1,
                "energy_impact": -0.1,
                "outcome_weights": {"productive": 0.6, "neutral": 0.3, "waste": 0.1}
            },
            "planning": {
                "duration_range": (45, 120),
                "effectiveness_bias": 0.2,
                "energy_impact": 0.0,
                "outcome_weights": {"productive": 0.7, "neutral": 0.2, "waste": 0.1}
            },
            "social": {
                "duration_range": (30, 60),
                "effectiveness_bias": -0.1,
                "energy_impact": 0.2,
                "outcome_weights": {"productive": 0.4, "neutral": 0.5, "waste": 0.1}
            }
        }
        
    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    def create_demo_users(self, conn) -> List[str]:
        """Create demo users and return their IDs"""
        cursor = conn.cursor()
        user_ids = []
        
        print("👥 Creating demo users...")
        
        for profile in self.user_profiles:
            user_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (cognito_sub) DO UPDATE SET
                    email = EXCLUDED.email,
                    full_name = EXCLUDED.full_name,
                    preferences = EXCLUDED.preferences,
                    updated_at = EXCLUDED.updated_at
                RETURNING id;
            """, (
                user_id,
                profile["cognito_sub"],
                profile["email"], 
                profile["name"],
                f'{{"pattern": "{profile["pattern"]}"}}',  # JSON preferences
                True,
                datetime.utcnow(),
                datetime.utcnow()
            ))
            
            result = cursor.fetchone()
            actual_user_id = result[0] if result else user_id
            user_ids.append(actual_user_id)
            
            print(f"  ✅ Created user: {profile['name']} ({profile['pattern']})")
        
        conn.commit()
        cursor.close()
        return user_ids
    
    def generate_events_for_user(self, user_id: str, profile: Dict, start_date: datetime, days: int) -> List[Dict]:
        """Generate events for a specific user based on their profile"""
        events = []
        current_date = start_date
        
        # Calculate improvement factor for 'improver' pattern
        improvement_factor = 0.0
        if profile["pattern"] == "improver":
            improvement_factor = 0.3 / days  # 0.3 point improvement over the period
        
        for day in range(days):
            # Skip weekends for most patterns (except some Friday meetings)
            if current_date.weekday() >= 5:  # Saturday, Sunday
                if random.random() > 0.1:  # 10% chance of weekend meetings
                    current_date += timedelta(days=1)
                    continue
            
            # Generate 2-6 meetings per day based on user pattern
            if profile["pattern"] == "high_performer":
                daily_meetings = random.randint(3, 6)
            elif profile["pattern"] == "inconsistent": 
                daily_meetings = random.randint(1, 8)  # Very variable
            else:
                daily_meetings = random.randint(2, 5)
            
            # Adjust for preferred days
            day_multiplier = 1.0
            if current_date.weekday() in profile["preferences"]["preferred_days"]:
                day_multiplier = 1.2
            else:
                day_multiplier = 0.7
            
            daily_meetings = int(daily_meetings * day_multiplier)
            
            # Generate meetings for this day
            used_hours = set()
            for meeting_num in range(daily_meetings):
                event = self.generate_single_event(
                    user_id, profile, current_date, used_hours, day, improvement_factor
                )
                if event:
                    events.append(event)
                    used_hours.add(event["start_time"].hour)
            
            current_date += timedelta(days=1)
        
        return events
    
    def generate_single_event(self, user_id: str, profile: Dict, date: datetime, 
                            used_hours: set, day_number: int, improvement_factor: float) -> Dict:
        """Generate a single event with realistic analytics data"""
        
        # Choose meeting type based on user preferences
        preferred_types = profile["preferences"]["meeting_types"]
        if random.random() < 0.7:  # 70% chance of preferred type
            meeting_type = random.choice(preferred_types)
        else:
            meeting_type = random.choice(list(self.meeting_types.keys()))
        
        # Choose time based on user's preferred hours
        peak_hours = profile["preferences"]["peak_hours"]
        low_energy_hours = profile["preferences"]["low_energy"]
        
        # Weight hour selection
        hour_weights = {}
        for hour in range(8, 19):  # 8 AM to 7 PM
            if hour in used_hours:
                continue
            if hour in peak_hours:
                hour_weights[hour] = 3.0
            elif hour in low_energy_hours:
                hour_weights[hour] = 0.5
            else:
                hour_weights[hour] = 1.0
        
        if not hour_weights:
            return None  # No available hours
        
        # Select hour based on weights
        hours = list(hour_weights.keys())
        weights = list(hour_weights.values())
        selected_hour = random.choices(hours, weights=weights)[0]
        
        # Generate start time
        start_time = date.replace(
            hour=selected_hour,
            minute=random.choice([0, 15, 30, 45]),
            second=0,
            microsecond=0
        )
        
        # Generate duration based on meeting type
        duration_range = self.meeting_types[meeting_type]["duration_range"]
        planned_duration = random.randint(duration_range[0], duration_range[1])
        
        # Actual duration (85-115% of planned, with some variability)
        duration_variance = random.uniform(0.85, 1.15)
        actual_duration = int(planned_duration * duration_variance)
        
        end_time = start_time + timedelta(minutes=actual_duration)
        
        # Calculate effectiveness rating based on multiple factors
        base_effectiveness = profile["preferences"]["avg_effectiveness"]
        
        # Apply time-of-day modifier
        time_modifier = 0.0
        if selected_hour in peak_hours:
            time_modifier = 0.5
        elif selected_hour in low_energy_hours:
            time_modifier = -0.4
        
        # Apply meeting type bias
        type_bias = self.meeting_types[meeting_type]["effectiveness_bias"]
        
        # Apply improvement factor over time
        time_improvement = improvement_factor * day_number
        
        # Add some random variation
        random_variation = random.uniform(-0.3, 0.3)
        
        effectiveness_rating = base_effectiveness + time_modifier + type_bias + time_improvement + random_variation
        effectiveness_rating = max(1, min(5, round(effectiveness_rating)))
        
        # Calculate energy level
        base_energy = 3.5
        energy_consistency = profile["preferences"]["energy_consistency"]
        
        # Time of day impact
        if selected_hour in peak_hours:
            energy_modifier = 0.8
        elif selected_hour in low_energy_hours:
            energy_modifier = -0.6
        else:
            energy_modifier = 0.0
        
        # Meeting type impact
        energy_impact = self.meeting_types[meeting_type]["energy_impact"]
        
        # Add consistency-based variation
        if energy_consistency > 0.7:
            energy_variation = random.uniform(-0.2, 0.2)
        else:
            energy_variation = random.uniform(-0.6, 0.6)
        
        energy_level = base_energy + energy_modifier + energy_impact + energy_variation
        energy_level = max(1, min(5, round(energy_level)))
        
        # Determine meeting outcome based on effectiveness and weights
        outcome_weights = self.meeting_types[meeting_type]["outcome_weights"]
        
        # Modify weights based on effectiveness
        if effectiveness_rating >= 4:
            outcome_weights = {"productive": 0.8, "neutral": 0.15, "waste": 0.05}
        elif effectiveness_rating <= 2:
            outcome_weights = {"productive": 0.2, "neutral": 0.3, "waste": 0.5}
        
        meeting_outcome = random.choices(
            list(outcome_weights.keys()),
            weights=list(outcome_weights.values())
        )[0]
        
        # Determine creation method
        created_via_options = ["manual", "voice", "imported", "text"]
        created_via_weights = [0.6, 0.15, 0.15, 0.1]  # Most are manual
        created_via = random.choices(created_via_options, weights=created_via_weights)[0]
        
        # Generate priority level (existing field)
        if meeting_outcome == "productive" and effectiveness_rating >= 4:
            priority_level = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2])[0]
        elif meeting_outcome == "waste":
            priority_level = random.choices([3, 4, 5], weights=[0.2, 0.5, 0.3])[0]
        else:
            priority_level = 3  # Default medium
        
        # Generate titles based on meeting type
        titles = {
            "team_standup": ["Daily Standup", "Team Sync", "Morning Standup", "Sprint Check-in"],
            "one_on_one": ["1:1 with Manager", "Weekly Check-in", "Career Discussion", "Feedback Session"],
            "strategic": ["Strategic Planning", "Quarterly Review", "Vision Alignment", "Strategy Discussion"],
            "client_call": ["Client Meeting", "Customer Call", "Project Update", "Requirements Review"],
            "all_hands": ["All Hands Meeting", "Company Update", "Town Hall", "Leadership Address"],
            "training": ["Skills Training", "Professional Development", "Workshop", "Learning Session"],
            "brainstorm": ["Brainstorming Session", "Creative Discussion", "Ideation Meeting", "Innovation Workshop"],
            "review": ["Code Review", "Project Review", "Performance Review", "Design Review"],
            "planning": ["Sprint Planning", "Project Planning", "Timeline Review", "Resource Planning"],
            "social": ["Team Lunch", "Coffee Chat", "Social Hour", "Team Building"]
        }
        
        title = random.choice(titles.get(meeting_type, ["Meeting"]))
        
        return {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": title,
            "description": f"{meeting_type.replace('_', ' ').title()} - Generated demo data",
            "start_time": start_time,
            "end_time": end_time,
            "location": random.choice(["Conference Room A", "Zoom", "Office", "Conference Room B", None]),
            "is_all_day": False,
            "recurrence_rule": None,
            "priority_level": priority_level,
            "priority_confidence": random.uniform(0.6, 0.95),
            "classification_method": random.choice(["manual", "bert", "rule_based"]),
            "meeting_outcome": meeting_outcome,
            "effectiveness_rating": effectiveness_rating,
            "energy_level": energy_level,
            "created_via": created_via,
            "actual_duration": actual_duration,
            "planned_duration": planned_duration,
            "created_at": start_time - timedelta(days=random.randint(1, 7)),
            "updated_at": start_time - timedelta(days=random.randint(0, 3))
        }
    
    def insert_events(self, conn, events: List[Dict]):
        """Insert events into database"""
        cursor = conn.cursor()
        
        print(f"📅 Inserting {len(events)} events...")
        
        for event in events:
            cursor.execute("""
                INSERT INTO events (
                    id, user_id, title, description, start_time, end_time,
                    location, is_all_day, recurrence_rule, priority_level,
                    priority_confidence, classification_method, meeting_outcome,
                    effectiveness_rating, energy_level, created_via,
                    actual_duration, planned_duration, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                event["id"],
                event["user_id"], 
                event["title"],
                event["description"],
                event["start_time"],
                event["end_time"],
                event["location"],
                event["is_all_day"],
                event["recurrence_rule"],
                event["priority_level"],
                event["priority_confidence"],
                event["classification_method"],
                event["meeting_outcome"],
                event["effectiveness_rating"],
                event["energy_level"],
                event["created_via"],
                event["actual_duration"],
                event["planned_duration"],
                event["created_at"],
                event["updated_at"]
            ))
        
        conn.commit()
        cursor.close()
        print(f"  ✅ Successfully inserted {len(events)} events")
    
    def generate_analytics_demo_data(self, weeks: int = 8):
        """Generate complete analytics demo data"""
        print(f"🚀 Generating {weeks} weeks of analytics demo data...")
        
        conn = self.connect_db()
        if not conn:
            return
        
        try:
            # Create demo users
            user_ids = self.create_demo_users(conn)
            
            # Calculate date range (8 weeks ago to now)
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(weeks=weeks)
            days = weeks * 7
            
            print(f"📊 Generating events from {start_date.date()} to {end_date.date()}")
            
            # Generate events for each user
            all_events = []
            for i, user_id in enumerate(user_ids):
                profile = self.user_profiles[i]
                print(f"  👤 Generating events for {profile['name']} ({profile['pattern']})...")
                
                user_events = self.generate_events_for_user(user_id, profile, start_date, days)
                all_events.extend(user_events)
                
                print(f"    ✅ Generated {len(user_events)} events")
            
            # Insert all events
            self.insert_events(conn, all_events)
            
            # Generate summary statistics
            self.print_summary_statistics(conn, all_events)
            
        except Exception as e:
            print(f"❌ Error generating demo data: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def print_summary_statistics(self, conn, events: List[Dict]):
        """Print summary statistics of generated data"""
        print("\n📈 ANALYTICS DEMO DATA SUMMARY")
        print("=" * 50)
        
        # Basic counts
        total_events = len(events)
        total_users = len(self.user_profiles)
        
        print(f"👥 Users created: {total_users}")
        print(f"📅 Events created: {total_events}")
        print(f"📊 Avg events per user: {total_events // total_users}")
        
        # Meeting outcomes distribution
        outcomes = {}
        effectiveness_ratings = []
        energy_levels = []
        meeting_types = {}
        
        for event in events:
            outcome = event["meeting_outcome"]
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
            effectiveness_ratings.append(event["effectiveness_rating"])
            energy_levels.append(event["energy_level"])
            
            # Extract meeting type from title/description
            for mtype in self.meeting_types.keys():
                if mtype.replace('_', ' ').lower() in event["title"].lower():
                    meeting_types[mtype] = meeting_types.get(mtype, 0) + 1
                    break
        
        print(f"\n📋 Meeting Outcomes:")
        for outcome, count in outcomes.items():
            percentage = (count / total_events) * 100
            print(f"  {outcome.title()}: {count} ({percentage:.1f}%)")
        
        print(f"\n⭐ Effectiveness Ratings:")
        avg_effectiveness = sum(effectiveness_ratings) / len(effectiveness_ratings)
        print(f"  Average: {avg_effectiveness:.2f}/5")
        for rating in range(1, 6):
            count = effectiveness_ratings.count(rating)
            percentage = (count / len(effectiveness_ratings)) * 100
            print(f"  {rating}⭐: {count} ({percentage:.1f}%)")
        
        print(f"\n🔋 Energy Levels:")
        avg_energy = sum(energy_levels) / len(energy_levels)
        print(f"  Average: {avg_energy:.2f}/5")
        
        print(f"\n🎯 Top Meeting Types:")
        sorted_types = sorted(meeting_types.items(), key=lambda x: x[1], reverse=True)
        for mtype, count in sorted_types[:5]:
            percentage = (count / total_events) * 100
            print(f"  {mtype.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
        
        print(f"\n✅ Demo data generation complete!")
        print(f"🔗 Ready for Analytics Dashboard testing")


def main():
    """Main function to run demo data generation"""
    print("🎯 KairoCal Analytics Dashboard Demo Data Generator")
    print("=" * 60)
    
    generator = AnalyticsDemoDataGenerator()
    
    # Generate 8 weeks of demo data
    generator.generate_analytics_demo_data(weeks=8)


if __name__ == "__main__":
    main()
