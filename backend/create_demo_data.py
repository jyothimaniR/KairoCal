#!/usr/bin/env python3
"""
Demo Data Generation Script for KairoCal BERT Priority Classification System
Creates realistic calendar events with diverse priorities for testing and demonstrations

This script generates:
- 100+ diverse calendar events with various priority levels
- Realistic event descriptions for BERT training validation
- User behavior patterns for analytics testing
- Conflict scenarios for resolution testing
- Different event types (work, personal, meetings, etc.)

Usage:
    python create_demo_data.py --users 5 --events-per-user 25 --conflicts 10
"""

import argparse
import asyncio
import random
import sys
import os
from datetime import datetime, timedelta, time
from typing import List, Dict, Any, Tuple
import logging
import json
from dataclasses import dataclass, asdict

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class DemoEvent:
    """Demo event structure"""
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    event_type: str
    expected_priority: int
    tags: List[str]
    user_notes: str = ""

class DemoDataGenerator:
    """Generates realistic demo data for KairoCal testing"""
    
    def __init__(self):
        self.event_templates = self._load_event_templates()
        self.locations = self._load_locations()
        self.user_names = self._load_user_names()
        
    def _load_event_templates(self) -> Dict[str, List[Dict]]:
        """Load diverse event templates with varying priorities"""
        return {
            "critical_priority": [
                {
                    "title": "Emergency Board Meeting",
                    "description": "Urgent board meeting to address critical company issues. All executives must attend.",
                    "type": "meeting",
                    "duration_hours": 2,
                    "tags": ["urgent", "executive", "critical"],
                    "priority": 1
                },
                {
                    "title": "System Outage Response",
                    "description": "Critical system outage affecting all customers. Immediate response required from technical team.",
                    "type": "incident",
                    "duration_hours": 4,
                    "tags": ["emergency", "technical", "outage"],
                    "priority": 1
                },
                {
                    "title": "Hospital Emergency",
                    "description": "Emergency medical appointment that cannot be rescheduled.",
                    "type": "medical",
                    "duration_hours": 3,
                    "tags": ["medical", "emergency", "health"],
                    "priority": 1
                },
                {
                    "title": "Legal Compliance Deadline",
                    "description": "Final deadline for regulatory compliance submission. Missing this could result in penalties.",
                    "type": "legal",
                    "duration_hours": 8,
                    "tags": ["legal", "compliance", "deadline"],
                    "priority": 1
                },
                {
                    "title": "Product Launch Crisis",
                    "description": "Critical issues discovered before major product launch. Emergency team meeting required.",
                    "type": "project",
                    "duration_hours": 6,
                    "tags": ["product", "launch", "crisis"],
                    "priority": 1
                }
            ],
            "high_priority": [
                {
                    "title": "Client Presentation",
                    "description": "Important presentation to key client for potential multi-million dollar contract.",
                    "type": "meeting",
                    "duration_hours": 2,
                    "tags": ["client", "presentation", "important"],
                    "priority": 2
                },
                {
                    "title": "Job Interview",
                    "description": "Final round interview for senior position at Fortune 500 company.",
                    "type": "interview",
                    "duration_hours": 1.5,
                    "tags": ["career", "interview", "opportunity"],
                    "priority": 2
                },
                {
                    "title": "Quarterly Review Meeting",
                    "description": "Quarterly performance review with manager. Important for career advancement.",
                    "type": "review",
                    "duration_hours": 1,
                    "tags": ["performance", "review", "career"],
                    "priority": 2
                },
                {
                    "title": "Doctor Appointment",
                    "description": "Important medical checkup that has been scheduled months in advance.",
                    "type": "medical",
                    "duration_hours": 1,
                    "tags": ["health", "medical", "checkup"],
                    "priority": 2
                },
                {
                    "title": "Project Milestone Review",
                    "description": "Critical milestone review for major project with tight deadlines.",
                    "type": "project",
                    "duration_hours": 3,
                    "tags": ["project", "milestone", "deadline"],
                    "priority": 2
                }
            ],
            "medium_priority": [
                {
                    "title": "Team Meeting",
                    "description": "Regular weekly team standup to discuss project progress and blockers.",
                    "type": "meeting",
                    "duration_hours": 1,
                    "tags": ["team", "standup", "regular"],
                    "priority": 3
                },
                {
                    "title": "Training Session",
                    "description": "Professional development training on new technologies and methodologies.",
                    "type": "training",
                    "duration_hours": 4,
                    "tags": ["training", "development", "skills"],
                    "priority": 3
                },
                {
                    "title": "Lunch Meeting",
                    "description": "Business lunch with potential partner to discuss collaboration opportunities.",
                    "type": "meeting",
                    "duration_hours": 1.5,
                    "tags": ["business", "lunch", "networking"],
                    "priority": 3
                },
                {
                    "title": "Code Review Session",
                    "description": "Scheduled code review session for recent feature implementation.",
                    "type": "review",
                    "duration_hours": 2,
                    "tags": ["code", "review", "development"],
                    "priority": 3
                },
                {
                    "title": "Budget Planning",
                    "description": "Annual budget planning session for department resource allocation.",
                    "type": "planning",
                    "duration_hours": 3,
                    "tags": ["budget", "planning", "finance"],
                    "priority": 3
                }
            ],
            "low_priority": [
                {
                    "title": "Coffee Chat",
                    "description": "Informal coffee meeting with colleague to catch up and discuss ideas.",
                    "type": "social",
                    "duration_hours": 0.5,
                    "tags": ["social", "coffee", "informal"],
                    "priority": 4
                },
                {
                    "title": "Office Happy Hour",
                    "description": "Optional team happy hour to celebrate recent project completion.",
                    "type": "social",
                    "duration_hours": 2,
                    "tags": ["social", "celebration", "optional"],
                    "priority": 4
                },
                {
                    "title": "Online Webinar",
                    "description": "Industry webinar on emerging trends. Interesting but not essential.",
                    "type": "learning",
                    "duration_hours": 1,
                    "tags": ["webinar", "learning", "industry"],
                    "priority": 4
                },
                {
                    "title": "Gym Session",
                    "description": "Regular workout session to maintain fitness and health.",
                    "type": "fitness",
                    "duration_hours": 1.5,
                    "tags": ["fitness", "health", "personal"],
                    "priority": 4
                },
                {
                    "title": "Book Club Meeting",
                    "description": "Monthly book club discussion with colleagues from different departments.",
                    "type": "social",
                    "duration_hours": 1,
                    "tags": ["books", "social", "monthly"],
                    "priority": 4
                }
            ],
            "very_low_priority": [
                {
                    "title": "Office Plant Watering",
                    "description": "Weekly task to water the office plants. Can be done anytime during the week.",
                    "type": "task",
                    "duration_hours": 0.25,
                    "tags": ["plants", "office", "flexible"],
                    "priority": 5
                },
                {
                    "title": "Personal Email Cleanup",
                    "description": "Organize and clean up personal email inbox. No deadline.",
                    "type": "personal",
                    "duration_hours": 1,
                    "tags": ["email", "organization", "personal"],
                    "priority": 5
                },
                {
                    "title": "YouTube Learning Videos",
                    "description": "Watch educational videos on topics of interest. Flexible timing.",
                    "type": "learning",
                    "duration_hours": 2,
                    "tags": ["video", "learning", "flexible"],
                    "priority": 5
                },
                {
                    "title": "Social Media Break",
                    "description": "Quick break to check social media and personal messages.",
                    "type": "break",
                    "duration_hours": 0.5,
                    "tags": ["social", "break", "personal"],
                    "priority": 5
                },
                {
                    "title": "Organize Desk",
                    "description": "Tidy up workspace and organize files. Can be done anytime.",
                    "type": "organization",
                    "duration_hours": 0.5,
                    "tags": ["organization", "workspace", "flexible"],
                    "priority": 5
                }
            ]
        }
    
    def _load_locations(self) -> List[str]:
        """Load diverse meeting locations"""
        return [
            "Conference Room A",
            "Conference Room B", 
            "CEO Office",
            "Meeting Room 101",
            "Boardroom",
            "Video Conference",
            "Zoom Call",
            "Client Office",
            "Restaurant Downtown",
            "Coffee Shop",
            "Home Office",
            "Coworking Space",
            "Training Center",
            "Hotel Conference Room",
            "Outdoor Meeting Area",
            "Library",
            "University Campus",
            "Hospital",
            "Gym",
            "Park"
        ]
    
    def _load_user_names(self) -> List[str]:
        """Load demo user names"""
        return [
            "Alice Johnson",
            "Bob Smith", 
            "Carol Davis",
            "David Wilson",
            "Emma Brown",
            "Frank Miller",
            "Grace Lee",
            "Henry Taylor",
            "Ivy Chen",
            "Jack Anderson"
        ]
    
    def generate_user_events(self, user_id: int, num_events: int = 25) -> List[DemoEvent]:
        """Generate events for a specific user"""
        logger.info(f"🎭 Generating {num_events} events for user {user_id}")
        
        events = []
        base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        # Priority distribution (more medium, fewer critical)
        priority_weights = {1: 0.1, 2: 0.2, 3: 0.4, 4: 0.2, 5: 0.1}
        
        for i in range(num_events):
            # Select priority based on weights
            priority = random.choices(
                list(priority_weights.keys()), 
                weights=list(priority_weights.values())
            )[0]
            
            # Get priority category
            priority_categories = {
                1: "critical_priority",
                2: "high_priority", 
                3: "medium_priority",
                4: "low_priority",
                5: "very_low_priority"
            }
            
            category = priority_categories[priority]
            template = random.choice(self.event_templates[category])
            
            # Generate timing (spread over next 30 days)
            days_offset = random.randint(0, 30)
            hour_offset = random.randint(0, 9)  # Business hours variance
            
            start_time = base_date + timedelta(
                days=days_offset,
                hours=hour_offset
            )
            
            duration = timedelta(hours=template["duration_hours"])
            end_time = start_time + duration
            
            # Add some realistic variations
            title_variations = self._add_title_variations(template["title"], user_id)
            description_variations = self._add_description_variations(template["description"])
            
            event = DemoEvent(
                title=title_variations,
                description=description_variations,
                start_time=start_time,
                end_time=end_time,
                location=random.choice(self.locations),
                event_type=template["type"],
                expected_priority=priority,
                tags=template["tags"],
                user_notes=self._generate_user_notes(template)
            )
            
            events.append(event)
        
        # Sort events by start time
        events.sort(key=lambda x: x.start_time)
        
        logger.info(f"✅ Generated {len(events)} events with priority distribution: "
                   f"P1:{len([e for e in events if e.expected_priority==1])}, "
                   f"P2:{len([e for e in events if e.expected_priority==2])}, "
                   f"P3:{len([e for e in events if e.expected_priority==3])}, "
                   f"P4:{len([e for e in events if e.expected_priority==4])}, "
                   f"P5:{len([e for e in events if e.expected_priority==5])}")
        
        return events
    
    def _add_title_variations(self, base_title: str, user_id: int) -> str:
        """Add realistic variations to event titles"""
        variations = [
            f"{base_title}",
            f"{base_title} - Week {random.randint(1, 52)}",
            f"{base_title} (Follow-up)",
            f"Q{random.randint(1, 4)} {base_title}",
            f"{base_title} - User{user_id}",
            f"Rescheduled: {base_title}"
        ]
        return random.choice(variations)
    
    def _add_description_variations(self, base_description: str) -> str:
        """Add realistic variations to descriptions"""
        additions = [
            "",
            " Please bring relevant documents.",
            " Agenda will be shared 24 hours in advance.",
            " Remote participants welcome via video call.",
            " Light refreshments will be provided.",
            " Preparation materials attached.",
            " Follow-up actions will be documented.",
            " Recording available for those who cannot attend."
        ]
        return base_description + random.choice(additions)
    
    def _generate_user_notes(self, template: Dict) -> str:
        """Generate realistic user notes"""
        notes_options = [
            "Important - do not reschedule",
            "Can be moved if necessary",
            "Tentative - waiting for confirmation", 
            "High priority for this week",
            "Flexible timing",
            "Requires preparation time",
            "May run longer than scheduled",
            "Critical for project success",
            "",  # No notes
            "Reminder set for 1 hour before"
        ]
        return random.choice(notes_options)
    
    def generate_conflict_scenarios(self, events: List[DemoEvent], num_conflicts: int = 10) -> List[DemoEvent]:
        """Generate intentional conflicts for testing conflict resolution"""
        logger.info(f"⚡ Creating {num_conflicts} conflict scenarios")
        
        conflict_events = []
        existing_events = events.copy()
        
        for i in range(num_conflicts):
            # Select a random existing event to conflict with
            target_event = random.choice(existing_events)
            
            # Create conflicting event with different priority
            priority_options = [p for p in [1, 2, 3, 4, 5] if p != target_event.expected_priority]
            conflict_priority = random.choice(priority_options)
            
            # Get template for the conflict priority
            priority_categories = {
                1: "critical_priority",
                2: "high_priority",
                3: "medium_priority", 
                4: "low_priority",
                5: "very_low_priority"
            }
            
            category = priority_categories[conflict_priority]
            template = random.choice(self.event_templates[category])
            
            # Create overlapping time
            overlap_start = target_event.start_time + timedelta(minutes=random.randint(-30, 30))
            duration = timedelta(hours=template["duration_hours"])
            overlap_end = overlap_start + duration
            
            conflict_event = DemoEvent(
                title=f"CONFLICT: {template['title']}",
                description=f"[DEMO CONFLICT] {template['description']} This event intentionally conflicts with '{target_event.title}' for testing.",
                start_time=overlap_start,
                end_time=overlap_end,
                location=random.choice(self.locations),
                event_type=template["type"],
                expected_priority=conflict_priority,
                tags=template["tags"] + ["conflict_test"],
                user_notes="Demo conflict scenario for testing resolution"
            )
            
            conflict_events.append(conflict_event)
        
        logger.info(f"✅ Created {len(conflict_events)} conflict scenarios")
        return conflict_events
    
    def export_demo_data(self, events: List[DemoEvent], filename: str = "demo_events.json"):
        """Export demo events to JSON file"""
        logger.info(f"💾 Exporting demo data to {filename}")
        
        # Convert events to serializable format
        events_data = []
        for event in events:
            event_dict = asdict(event)
            # Convert datetime objects to ISO strings
            event_dict['start_time'] = event.start_time.isoformat()
            event_dict['end_time'] = event.end_time.isoformat()
            events_data.append(event_dict)
        
        # Add metadata
        export_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_events": len(events),
                "priority_distribution": {
                    str(p): len([e for e in events if e.expected_priority == p])
                    for p in [1, 2, 3, 4, 5]
                },
                "date_range": {
                    "start": min(events, key=lambda x: x.start_time).start_time.isoformat(),
                    "end": max(events, key=lambda x: x.start_time).start_time.isoformat()
                },
                "event_types": list(set(e.event_type for e in events))
            },
            "events": events_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Demo data exported successfully to {filename}")
        return export_data
    
    def generate_priority_validation_set(self) -> List[DemoEvent]:
        """Generate a specific set of events for BERT priority validation"""
        logger.info("🧪 Generating priority validation test set")
        
        validation_events = []
        
        # High-confidence priority examples
        test_cases = [
            {
                "title": "Server Down - Critical Production Issue",
                "description": "Production servers are completely down affecting all customers. Revenue loss of $10k per hour. All hands on deck required immediately.",
                "expected_priority": 1,
                "tags": ["emergency", "production", "revenue"]
            },
            {
                "title": "Board Meeting for CEO Selection",
                "description": "Emergency board meeting to select new CEO after sudden resignation. Media attention and investor concerns require immediate action.",
                "expected_priority": 1,
                "tags": ["executive", "crisis", "urgent"]
            },
            {
                "title": "Client Proposal Presentation - $5M Deal",
                "description": "Final presentation to secure largest client contract in company history. Three months of preparation leading to this moment.",
                "expected_priority": 2,
                "tags": ["client", "revenue", "important"]
            },
            {
                "title": "Team Lunch - Pizza Friday",
                "description": "Regular team bonding over pizza. Nice to have but not critical for business operations.",
                "expected_priority": 4,
                "tags": ["social", "team", "food"]
            },
            {
                "title": "Clean Out Old Files",
                "description": "Organize old files in shared drive. Been postponed for months, can wait longer if needed.",
                "expected_priority": 5,
                "tags": ["organization", "maintenance", "optional"]
            }
        ]
        
        base_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        for i, case in enumerate(test_cases):
            event = DemoEvent(
                title=case["title"],
                description=case["description"],
                start_time=base_time + timedelta(hours=i*2),
                end_time=base_time + timedelta(hours=i*2 + 1),
                location="Test Location",
                event_type="validation",
                expected_priority=case["expected_priority"],
                tags=case["tags"],
                user_notes="Priority validation test case"
            )
            validation_events.append(event)
        
        logger.info(f"✅ Generated {len(validation_events)} priority validation test cases")
        return validation_events

async def main():
    """Main demo data generation function"""
    parser = argparse.ArgumentParser(description="Generate demo data for KairoCal BERT testing")
    parser.add_argument("--users", type=int, default=3, help="Number of demo users")
    parser.add_argument("--events-per-user", type=int, default=20, help="Events per user")
    parser.add_argument("--conflicts", type=int, default=5, help="Number of conflict scenarios")
    parser.add_argument("--output", type=str, default="demo_events.json", help="Output filename")
    parser.add_argument("--validation-only", action="store_true", help="Generate only validation test set")
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting KairoCal Demo Data Generation")
    logger.info(f"📊 Configuration: {args.users} users, {args.events_per_user} events each, {args.conflicts} conflicts")
    
    generator = DemoDataGenerator()
    all_events = []
    
    if args.validation_only:
        # Generate only validation set
        validation_events = generator.generate_priority_validation_set()
        all_events.extend(validation_events)
        logger.info(f"✅ Generated validation set with {len(validation_events)} events")
    else:
        # Generate events for each user
        for user_id in range(1, args.users + 1):
            user_events = generator.generate_user_events(user_id, args.events_per_user)
            all_events.extend(user_events)
        
        # Add conflict scenarios
        if args.conflicts > 0:
            conflict_events = generator.generate_conflict_scenarios(all_events, args.conflicts)
            all_events.extend(conflict_events)
        
        # Add validation set
        validation_events = generator.generate_priority_validation_set()
        all_events.extend(validation_events)
    
    # Export all data
    export_data = generator.export_demo_data(all_events, args.output)
    
    # Print summary
    total_events = len(all_events)
    priority_dist = {p: len([e for e in all_events if e.expected_priority == p]) for p in [1,2,3,4,5]}
    
    logger.info("📈 Demo Data Generation Complete!")
    logger.info(f"   Total Events: {total_events}")
    logger.info(f"   Priority Distribution: P1:{priority_dist[1]}, P2:{priority_dist[2]}, P3:{priority_dist[3]}, P4:{priority_dist[4]}, P5:{priority_dist[5]}")
    logger.info(f"   Output File: {args.output}")
    logger.info(f"   Date Range: {export_data['metadata']['date_range']['start'][:10]} to {export_data['metadata']['date_range']['end'][:10]}")
    
    print(f"\n🎉 Success! Generated {total_events} demo events")
    print(f"📁 Data saved to: {args.output}")
    print("\n📋 Next steps:")
    print("1. Run BERT training with: python train_bert_model.py")
    print("2. Test pipeline with: python test_full_event_pipeline.py")
    print("3. Start the API server: uvicorn app.main:app --reload")
    print("4. Test priority classification via API endpoints")

if __name__ == "__main__":
    asyncio.run(main())
