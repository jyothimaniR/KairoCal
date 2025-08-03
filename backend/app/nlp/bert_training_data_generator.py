# backend/app/nlp/bert_training_data_generator.py
"""
Advanced Training Data Generator for BERT Priority Classification
Creates realistic, diverse training examples for event priority classification
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import numpy as np

class BERTTrainingDataGenerator:
    """
    Generates high-quality training data for BERT priority classification
    
    Features:
    - Realistic event scenarios
    - Balanced priority distribution
    - Temporal diversity
    - Location variety
    - Contextual complexity
    """
    
    def __init__(self):
        self.priority_templates = self._initialize_priority_templates()
        self.locations = self._initialize_locations()
        self.time_patterns = self._initialize_time_patterns()
        
    def _initialize_priority_templates(self) -> Dict[int, List[Dict]]:
        """Initialize templates for each priority level"""
        return {
            5: [  # Critical Priority
                {
                    "title_templates": [
                        "URGENT: CEO Meeting",
                        "CRITICAL: System Outage Response",
                        "EMERGENCY: Data Breach Meeting",
                        "ASAP: Crisis Management",
                        "URGENT: Board Meeting",
                        "CRITICAL: Client Escalation",
                        "EMERGENCY: Security Incident",
                        "URGENT: Investor Call",
                        "CRITICAL: Production Issue",
                        "ASAP: Legal Review"
                    ],
                    "description_templates": [
                        "Critical deadline - requires immediate attention",
                        "Emergency response needed for system failure",
                        "Urgent escalation from major client",
                        "Time-sensitive legal matter",
                        "Crisis communication strategy session",
                        "Board requires immediate update",
                        "Critical bug affecting all users",
                        "Emergency investor relations call",
                        "Regulatory compliance deadline",
                        "Critical security vulnerability"
                    ],
                    "contexts": ["crisis", "emergency", "urgent", "critical"]
                }
            ],
            4: [  # High Priority
                {
                    "title_templates": [
                        "Important: Project Deadline Review",
                        "Client Presentation",
                        "Executive Interview",
                        "Important: Budget Approval",
                        "Key Stakeholder Meeting",
                        "Important: Product Launch",
                        "Director Review",
                        "Important: Contract Negotiation",
                        "Quarterly Business Review",
                        "Important: Team Performance Review"
                    ],
                    "description_templates": [
                        "Important milestone for Q4 delivery",
                        "Key presentation to major client",
                        "Executive decision required",
                        "Important budget planning session",
                        "Strategic review with stakeholders",
                        "Product launch preparation",
                        "Performance review with director",
                        "Contract terms negotiation",
                        "Quarterly goals assessment",
                        "Team development planning"
                    ],
                    "contexts": ["important", "strategic", "executive", "milestone"]
                }
            ],
            3: [  # Medium Priority
                {
                    "title_templates": [
                        "Team Meeting",
                        "Project Planning Session",
                        "Weekly Standup",
                        "Training Workshop",
                        "Team Review",
                        "Project Sync",
                        "Department Meeting",
                        "Work Planning",
                        "Status Update Meeting",
                        "Team Building"
                    ],
                    "description_templates": [
                        "Regular team synchronization",
                        "Project planning and coordination",
                        "Weekly progress review",
                        "Professional development training",
                        "Team collaboration session",
                        "Project status update",
                        "Department coordination meeting",
                        "Work planning for next sprint",
                        "Regular status check-in",
                        "Team building activity"
                    ],
                    "contexts": ["regular", "team", "planning", "coordination"]
                }
            ],
            2: [  # Low Priority
                {
                    "title_templates": [
                        "Lunch with Colleagues",
                        "Personal Development",
                        "Coffee Chat",
                        "Social Event",
                        "Personal Appointment",
                        "Casual Meeting",
                        "Lunch Break",
                        "Social Gathering",
                        "Personal Time",
                        "Networking Event"
                    ],
                    "description_templates": [
                        "Casual lunch with team members",
                        "Personal skill development session",
                        "Informal coffee discussion",
                        "Social team gathering",
                        "Personal appointment scheduling",
                        "Casual conversation and networking",
                        "Regular lunch break",
                        "Social networking opportunity",
                        "Personal time for reflection",
                        "Professional networking event"
                    ],
                    "contexts": ["casual", "social", "personal", "informal"]
                }
            ],
            1: [  # Very Low Priority
                {
                    "title_templates": [
                        "Coffee Break",
                        "Optional Workshop",
                        "Free Time",
                        "Casual Chat",
                        "Break Time",
                        "Optional Event",
                        "Leisure Activity",
                        "Personal Break",
                        "Optional Meeting",
                        "Free Period"
                    ],
                    "description_templates": [
                        "Short coffee break",
                        "Optional professional development",
                        "Free time for personal tasks",
                        "Casual conversation opportunity",
                        "Regular break time",
                        "Optional attendance event",
                        "Personal leisure activity",
                        "Short personal break",
                        "Optional team discussion",
                        "Free period for catching up"
                    ],
                    "contexts": ["optional", "break", "leisure", "flexible"]
                }
            ]
        }
        
    def _initialize_locations(self) -> Dict[str, List[str]]:
        """Initialize location templates by category"""
        return {
            "office": [
                "Conference Room A", "Meeting Room 205", "Office Building",
                "Boardroom", "Main Office", "Corporate Headquarters",
                "Executive Suite", "Team Room", "Open Office Area"
            ],
            "remote": [
                "Zoom Meeting", "Microsoft Teams", "Google Meet",
                "Remote Call", "Virtual Meeting", "Online Conference",
                "Video Call", "Webinar", "Virtual Workshop"
            ],
            "restaurant": [
                "Restaurant Downtown", "Café Central", "Lunch Spot",
                "Italian Restaurant", "Coffee Shop", "Business Lunch Venue",
                "Local Bistro", "Corporate Dining", "Lunch Meeting Place"
            ],
            "external": [
                "Client Office", "Hotel Conference Room", "Convention Center",
                "Airport Lounge", "Co-working Space", "Business Center",
                "Training Facility", "Event Venue", "Off-site Location"
            ],
            "medical": [
                "Medical Clinic", "Doctor's Office", "Hospital",
                "Dental Office", "Health Center", "Medical Appointment"
            ],
            "personal": [
                "Home", "Personal Location", "Private Office",
                "Study Room", "Personal Space"
            ]
        }
        
    def _initialize_time_patterns(self) -> Dict[str, List[Tuple[int, int]]]:
        """Initialize time patterns for different priority levels"""
        return {
            "urgent": [(0, 23)],  # Any time for urgent
            "business": [(9, 17)],  # Business hours
            "extended": [(7, 19)],  # Extended business hours
            "evening": [(17, 21)],  # Evening
            "flexible": [(8, 20)]   # Flexible hours
        }
        
    def generate_training_example(self, priority: int) -> Dict[str, Any]:
        """Generate a single training example for specified priority"""
        templates = self.priority_templates[priority][0]
        
        # Select random title and description
        title = random.choice(templates["title_templates"])
        description = random.choice(templates["description_templates"])
        
        # Add variation to title and description
        title = self._add_variation(title, priority)
        description = self._add_variation(description, priority)
        
        # Generate temporal data
        start_time, end_time = self._generate_time_data(priority)
        
        # Generate location
        location = self._generate_location(priority)
        
        return {
            "title": title,
            "description": description,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "location": location,
            "priority": priority,
            "is_all_day": random.choice([True, False]) if random.random() < 0.1 else False
        }
        
    def _add_variation(self, text: str, priority: int) -> str:
        """Add contextual variation to text based on priority"""
        variations = {
            5: ["URGENT", "CRITICAL", "ASAP", "EMERGENCY", "HIGH PRIORITY"],
            4: ["Important", "Key", "Strategic", "Major", "Significant"],
            3: ["Regular", "Scheduled", "Planned", "Team", "Standard"],
            2: ["Casual", "Informal", "Social", "Personal", "Flexible"],
            1: ["Optional", "Flexible", "Free", "Casual", "Break"]
        }
        
        if random.random() < 0.3:  # 30% chance to add variation
            prefix = random.choice(variations[priority])
            if not any(word in text.upper() for word in ["URGENT", "CRITICAL", "IMPORTANT"]):
                text = f"{prefix}: {text}"
                
        return text
        
    def _generate_time_data(self, priority: int) -> Tuple[datetime, datetime]:
        """Generate realistic start and end times based on priority"""
        base_date = datetime.now() + timedelta(days=random.randint(1, 30))
        
        # Priority affects time constraints
        if priority >= 4:  # High/Critical priority
            # More likely during business hours, shorter notice
            hour = random.choice(range(9, 18))
            base_date = datetime.now() + timedelta(days=random.randint(0, 7))
        elif priority == 3:  # Medium priority
            # Business hours preferred
            hour = random.choice(range(8, 19))
        else:  # Low priority
            # More flexible timing
            hour = random.choice(range(7, 21))
            
        start_time = base_date.replace(
            hour=hour,
            minute=random.choice([0, 15, 30, 45]),
            second=0,
            microsecond=0
        )
        
        # Duration varies by priority
        duration_options = {
            5: [0.5, 1, 1.5, 2],      # Critical: short, focused
            4: [1, 1.5, 2, 2.5],      # High: moderate duration
            3: [1, 1.5, 2, 3],        # Medium: standard duration
            2: [1, 1.5, 2, 3, 4],     # Low: flexible duration
            1: [0.5, 1, 2]            # Very low: short or flexible
        }
        
        duration = random.choice(duration_options[priority])
        end_time = start_time + timedelta(hours=duration)
        
        return start_time, end_time
        
    def _generate_location(self, priority: int) -> str:
        """Generate appropriate location based on priority"""
        location_preferences = {
            5: ["office", "remote"],           # Critical: office or urgent remote
            4: ["office", "external", "remote"], # High: professional locations
            3: ["office", "remote"],           # Medium: standard locations
            2: ["restaurant", "office", "personal"], # Low: casual locations
            1: ["personal", "restaurant"]      # Very low: flexible locations
        }
        
        category = random.choice(location_preferences[priority])
        return random.choice(self.locations[category])
        
    def generate_training_dataset(self, 
                                size: int = 2000, 
                                balanced: bool = True) -> List[Dict[str, Any]]:
        """
        Generate a complete training dataset
        
        Args:
            size: Total number of examples to generate
            balanced: Whether to balance examples across priority levels
            
        Returns:
            List of training examples
        """
        examples = []
        
        if balanced:
            # Equal distribution across priorities
            per_priority = size // 5
            for priority in range(1, 6):
                for _ in range(per_priority):
                    examples.append(self.generate_training_example(priority))
        else:
            # Realistic distribution (more medium priority events)
            priority_weights = [0.15, 0.20, 0.30, 0.25, 0.10]  # 1-5 priorities
            for _ in range(size):
                priority = np.random.choice(range(1, 6), p=priority_weights)
                examples.append(self.generate_training_example(priority))
                
        # Shuffle the examples
        random.shuffle(examples)
        
        return examples
        
    def generate_validation_scenarios(self) -> List[Dict[str, Any]]:
        """Generate specific validation scenarios for testing"""
        scenarios = [
            # Critical scenarios
            {
                "title": "URGENT: Production System Down",
                "description": "Critical system failure affecting all customers",
                "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=3)).isoformat(),
                "location": "Emergency Response Room",
                "expected_priority": 5
            },
            # High priority scenarios
            {
                "title": "Important: Board Presentation",
                "description": "Quarterly results presentation to board of directors",
                "start_time": (datetime.now() + timedelta(days=2)).isoformat(),
                "end_time": (datetime.now() + timedelta(days=2, hours=2)).isoformat(),
                "location": "Boardroom",
                "expected_priority": 4
            },
            # Medium priority scenarios
            {
                "title": "Team Planning Meeting",
                "description": "Sprint planning for next iteration",
                "start_time": (datetime.now() + timedelta(days=5)).isoformat(),
                "end_time": (datetime.now() + timedelta(days=5, hours=2)).isoformat(),
                "location": "Conference Room B",
                "expected_priority": 3
            },
            # Low priority scenarios
            {
                "title": "Lunch with Marketing Team",
                "description": "Casual lunch to discuss collaboration",
                "start_time": (datetime.now() + timedelta(days=7)).isoformat(),
                "end_time": (datetime.now() + timedelta(days=7, hours=1)).isoformat(),
                "location": "Local Restaurant",
                "expected_priority": 2
            },
            # Very low priority scenarios
            {
                "title": "Optional Training Session",
                "description": "Optional skill development workshop",
                "start_time": (datetime.now() + timedelta(days=10)).isoformat(),
                "end_time": (datetime.now() + timedelta(days=10, hours=1)).isoformat(),
                "location": "Training Room",
                "expected_priority": 1
            }
        ]
        
        return scenarios

    def analyze_dataset(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the generated dataset for quality and distribution
        
        Args:
            dataset: List of training examples
            
        Returns:
            Analysis results
        """
        analysis = {
            "total_examples": len(dataset),
            "priority_distribution": {},
            "location_distribution": {},
            "time_distribution": {},
            "duration_stats": {},
            "text_stats": {}
        }
        
        # Priority distribution
        for example in dataset:
            priority = example["priority"]
            analysis["priority_distribution"][priority] = analysis["priority_distribution"].get(priority, 0) + 1
        
        # Location distribution
        location_categories = {}
        for example in dataset:
            location = example.get("location", "Unknown")
            # Categorize location
            for category, locations in self.locations.items():
                if location in locations:
                    location_categories[category] = location_categories.get(category, 0) + 1
                    break
        analysis["location_distribution"] = location_categories
        
        # Time distribution (by hour)
        hour_distribution = {}
        for example in dataset:
            try:
                start_time = datetime.fromisoformat(example["start_time"])
                hour = start_time.hour
                hour_distribution[hour] = hour_distribution.get(hour, 0) + 1
            except:
                pass
        analysis["time_distribution"] = hour_distribution
        
        # Duration statistics
        durations = []
        for example in dataset:
            try:
                start_time = datetime.fromisoformat(example["start_time"])
                end_time = datetime.fromisoformat(example["end_time"])
                duration = (end_time - start_time).total_seconds() / 3600  # hours
                durations.append(duration)
            except:
                pass
        
        if durations:
            analysis["duration_stats"] = {
                "mean": np.mean(durations),
                "median": np.median(durations),
                "min": min(durations),
                "max": max(durations),
                "std": np.std(durations)
            }
        
        # Text statistics
        title_lengths = []
        description_lengths = []
        for example in dataset:
            title_lengths.append(len(example.get("title", "")))
            description_lengths.append(len(example.get("description", "")))
        
        analysis["text_stats"] = {
            "avg_title_length": np.mean(title_lengths) if title_lengths else 0,
            "avg_description_length": np.mean(description_lengths) if description_lengths else 0,
            "total_unique_titles": len(set(ex.get("title", "") for ex in dataset)),
            "total_unique_descriptions": len(set(ex.get("description", "") for ex in dataset))
        }
        
        return analysis

    def save_training_data(self, dataset: List[Dict[str, Any]], filepath: str):
        """Save training data to JSON file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        print(f"Training data saved to {filepath}")

    def load_training_data(self, filepath: str) -> List[Dict[str, Any]]:
        """Load training data from JSON file"""
        with open(filepath, 'r') as f:
            dataset = json.load(f)
        
        print(f"Training data loaded from {filepath}")
        return dataset