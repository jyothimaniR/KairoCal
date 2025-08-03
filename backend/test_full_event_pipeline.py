# backend/test_full_event_pipeline.py
"""
Complete Event-to-Priority Flow Testing
Tests end-to-end event creation with BERT priority classification
"""

import sys
import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import get_settings
from app.models.event import Event
from app.models.user import User
from app.core.database import get_db
from app.nlp.nlp_service import NLPService
from app.nlp.model_loader import load_bert_model, is_trained_model_available
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventPipelineTester:
    """Comprehensive event creation and priority classification testing"""
    
    def __init__(self):
        self.settings = get_settings()
        self.priority_labels = {
            1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Very Low"
        }
        
        # Setup database session
        engine = create_engine(self.settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = SessionLocal()
        
        # Initialize NLP service
        self.nlp_service = NLPService()
        
    def create_test_user(self) -> User:
        """Create or get test user for event testing"""
        test_email = "test_pipeline@kairocal.com"
        
        # Check if user exists
        user = self.db.query(User).filter(User.email == test_email).first()
        
        if not user:
            user = User(
                email=test_email,
                full_name="Pipeline Test User",
                cognito_sub="test-pipeline-user-123",
                is_active=True
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info("✅ Created test user")
        else:
            logger.info("✅ Using existing test user")
            
        return user
    
    def get_test_events(self) -> List[Dict[str, Any]]:
        """Get comprehensive test event dataset"""
        base_time = datetime.now()
        
        test_events = [
            # Critical Priority (1)
            {
                "title": "URGENT: Server System Failure",
                "description": "Critical production system outage requiring immediate response",
                "start_time": base_time + timedelta(hours=1),
                "end_time": base_time + timedelta(hours=2),
                "location": "IT Operations Center",
                "expected_priority": 1,
                "category": "Critical Emergency"
            },
            {
                "title": "EMERGENCY: CEO Crisis Meeting",
                "description": "Emergency board meeting for crisis management",
                "start_time": base_time + timedelta(hours=2),
                "end_time": base_time + timedelta(hours=3),
                "location": "Executive Boardroom",
                "expected_priority": 1,
                "category": "Critical Business"
            },
            
            # High Priority (2)
            {
                "title": "Important: Client Presentation",
                "description": "Quarterly review presentation for major client account",
                "start_time": base_time + timedelta(days=1, hours=9),
                "end_time": base_time + timedelta(days=1, hours=11),
                "location": "Conference Room A",
                "expected_priority": 2,
                "category": "High Business"
            },
            {
                "title": "Executive Interview - VP Position",
                "description": "Final round interview for Vice President role",
                "start_time": base_time + timedelta(days=1, hours=14),
                "end_time": base_time + timedelta(days=1, hours=15),
                "location": "Executive Office",
                "expected_priority": 2,
                "category": "High HR"
            },
            
            # Medium Priority (3)
            {
                "title": "Weekly Team Meeting",
                "description": "Regular team sync and project status updates",
                "start_time": base_time + timedelta(days=2, hours=10),
                "end_time": base_time + timedelta(days=2, hours=11),
                "location": "Conference Room B",
                "expected_priority": 3,
                "category": "Medium Regular"
            },
            {
                "title": "Dentist Appointment",
                "description": "Routine dental checkup and cleaning",
                "start_time": base_time + timedelta(days=3, hours=15),
                "end_time": base_time + timedelta(days=3, hours=16),
                "location": "Dental Clinic",
                "expected_priority": 3,
                "category": "Medium Personal"
            },
            
            # Low Priority (4)
            {
                "title": "Team Lunch Social",
                "description": "Casual team lunch and bonding activity",
                "start_time": base_time + timedelta(days=4, hours=12),
                "end_time": base_time + timedelta(days=4, hours=13, minutes=30),
                "location": "Restaurant Downtown",
                "expected_priority": 4,
                "category": "Low Social"
            },
            {
                "title": "Optional Training Workshop",
                "description": "Professional development session on new technologies",
                "start_time": base_time + timedelta(days=5, hours=14),
                "end_time": base_time + timedelta(days=5, hours=17),
                "location": "Training Room",
                "expected_priority": 4,
                "category": "Low Development"
            },
            
            # Very Low Priority (5)
            {
                "title": "Coffee Break with Colleague",
                "description": "Informal chat and coffee with team member",
                "start_time": base_time + timedelta(days=6, hours=15),
                "end_time": base_time + timedelta(days=6, hours=15, minutes=30),
                "location": "Coffee Shop",
                "expected_priority": 5,
                "category": "Very Low Social"
            },
            {
                "title": "Personal Grocery Shopping",
                "description": "Weekly grocery shopping and errands",
                "start_time": base_time + timedelta(days=7, hours=10),
                "end_time": base_time + timedelta(days=7, hours=11),
                "location": "Grocery Store",
                "expected_priority": 5,
                "category": "Very Low Personal"
            }
        ]
        
        return test_events
    
    def test_priority_classification(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test priority classification for a single event"""
        try:
            # Test NLP service classification
            priority, confidence, method = self.nlp_service.classify_priority(event_data)
            
            result = {
                "event_title": event_data["title"],
                "predicted_priority": priority,
                "predicted_label": self.priority_labels[priority],
                "confidence": confidence,
                "classification_method": method,
                "expected_priority": event_data.get("expected_priority"),
                "success": True
            }
            
            # Check accuracy
            if "expected_priority" in event_data:
                result["correct"] = priority == event_data["expected_priority"]
                result["priority_difference"] = abs(priority - event_data["expected_priority"])
            
            return result
            
        except Exception as e:
            logger.error(f"Priority classification failed for '{event_data['title']}': {str(e)}")
            return {
                "event_title": event_data["title"],
                "error": str(e),
                "success": False
            }
    
    def test_event_creation_with_priority(self, user: User, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test complete event creation with priority classification"""
        try:
            # Classify priority first
            priority, confidence, method = self.nlp_service.classify_priority(event_data)
            
            # Create event with priority data
            event = Event(
                user_id=user.id,
                title=event_data["title"],
                description=event_data.get("description", ""),
                start_time=event_data["start_time"],
                end_time=event_data["end_time"],
                location=event_data.get("location"),
                priority_level=priority,
                priority_confidence=confidence,
                classification_method=method
            )
            
            # Save to database
            self.db.add(event)
            self.db.commit()
            self.db.refresh(event)
            
            result = {
                "event_id": str(event.id),
                "event_title": event.title,
                "stored_priority": event.priority_level,
                "stored_confidence": event.priority_confidence,
                "stored_method": event.classification_method,
                "predicted_priority": priority,
                "expected_priority": event_data.get("expected_priority"),
                "database_success": True,
                "classification_success": True
            }
            
            # Verify database storage
            retrieved_event = self.db.query(Event).filter(Event.id == event.id).first()
            if retrieved_event:
                result["database_verification"] = {
                    "priority_stored": retrieved_event.priority_level == priority,
                    "confidence_stored": retrieved_event.priority_confidence == confidence,
                    "method_stored": retrieved_event.classification_method == method
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Event creation failed for '{event_data['title']}': {str(e)}")
            return {
                "event_title": event_data["title"],
                "error": str(e),
                "database_success": False,
                "classification_success": False
            }
    
    def test_bert_vs_fallback_modes(self) -> Dict[str, Any]:
        """Test both BERT and fallback classification modes"""
        logger.info("🔄 Testing BERT vs Fallback classification modes...")
        
        test_event = {
            "title": "URGENT: System Critical Alert",
            "description": "Critical system alert requiring immediate attention",
            "expected_priority": 1
        }
        
        results = {}
        
        try:
            # Test current mode (BERT or fallback)
            classifier = load_bert_model()
            is_bert_mode = classifier.is_trained
            
            priority, confidence = classifier.predict(test_event)
            
            results["current_mode"] = {
                "mode": "BERT" if is_bert_mode else "Fallback",
                "priority": priority,
                "confidence": confidence,
                "model_available": is_trained_model_available()
            }
            
            # Test fallback mode explicitly
            if is_bert_mode:
                # Test rule-based classification
                fallback_priority, fallback_confidence = self.nlp_service._rule_based_priority_classification(test_event)
                results["fallback_mode"] = {
                    "mode": "Rule-based",
                    "priority": fallback_priority,
                    "confidence": fallback_confidence
                }
            
            logger.info(f"✅ Mode testing completed: Current={results['current_mode']['mode']}")
            
        except Exception as e:
            logger.error(f"❌ Mode testing failed: {str(e)}")
            results["error"] = str(e)
            
        return results
    
    def run_comprehensive_pipeline_test(self) -> Dict[str, Any]:
        """Run complete end-to-end pipeline testing"""
        logger.info("🚀 Starting Comprehensive Event Pipeline Testing")
        logger.info("=" * 70)
        
        test_start = datetime.now()
        results = {
            "test_start": test_start.isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "classification_results": [],
            "database_results": [],
            "mode_tests": {}
        }
        
        try:
            # Create test user
            user = self.create_test_user()
            
            # Get test events
            test_events = self.get_test_events()
            logger.info(f"📊 Testing {len(test_events)} events...")
            
            # Test 1: Priority Classification Only
            logger.info("\n1️⃣ Testing Priority Classification...")
            classification_correct = 0
            
            for event in test_events:
                result = self.test_priority_classification(event)
                results["classification_results"].append(result)
                results["tests_run"] += 1
                
                if result.get("success") and result.get("correct"):
                    classification_correct += 1
                    results["tests_passed"] += 1
                elif not result.get("success"):
                    results["tests_failed"] += 1
                
                status = "✅" if result.get("correct") else "❌" if not result.get("success") else "⚠️"
                logger.info(f"   {status} {event['category']:>15} | P{result.get('predicted_priority', 'X')} "
                          f"(Expected: P{event.get('expected_priority', 'X')}) | "
                          f"Conf: {result.get('confidence', 0):.3f}")
            
            classification_accuracy = classification_correct / len(test_events)
            logger.info(f"   📈 Classification Accuracy: {classification_accuracy:.2%}")
            
            # Test 2: Database Storage with Priority
            logger.info("\n2️⃣ Testing Database Storage with Priority...")
            database_success = 0
            
            for event in test_events[:5]:  # Test subset for database
                result = self.test_event_creation_with_priority(user, event)
                results["database_results"].append(result)
                results["tests_run"] += 1
                
                if result.get("database_success") and result.get("classification_success"):
                    database_success += 1
                    results["tests_passed"] += 1
                else:
                    results["tests_failed"] += 1
                
                status = "✅" if result.get("database_success") else "❌"
                logger.info(f"   {status} Database: {event['title'][:40]}... | "
                          f"P{result.get('stored_priority', 'X')} | "
                          f"Method: {result.get('stored_method', 'Unknown')}")
            
            database_accuracy = database_success / min(len(test_events), 5)
            logger.info(f"   📈 Database Storage Success: {database_accuracy:.2%}")
            
            # Test 3: BERT vs Fallback Modes
            logger.info("\n3️⃣ Testing BERT vs Fallback Modes...")
            mode_results = self.test_bert_vs_fallback_modes()
            results["mode_tests"] = mode_results
            results["tests_run"] += 1
            
            if "error" not in mode_results:
                results["tests_passed"] += 1
                logger.info(f"   ✅ Mode testing successful")
            else:
                results["tests_failed"] += 1
                logger.info(f"   ❌ Mode testing failed")
            
            # Calculate overall results
            test_duration = (datetime.now() - test_start).total_seconds()
            success_rate = results["tests_passed"] / results["tests_run"] if results["tests_run"] > 0 else 0
            
            results.update({
                "test_end": datetime.now().isoformat(),
                "duration_seconds": test_duration,
                "success_rate": success_rate,
                "classification_accuracy": classification_accuracy,
                "database_accuracy": database_accuracy,
                "overall_status": "PASSED" if success_rate >= 0.8 else "FAILED"
            })
            
            # Final summary
            logger.info("\n" + "=" * 70)
            logger.info("📊 PIPELINE TEST SUMMARY")
            logger.info("=" * 70)
            logger.info(f"✅ Tests Passed: {results['tests_passed']}")
            logger.info(f"❌ Tests Failed: {results['tests_failed']}")
            logger.info(f"📈 Success Rate: {success_rate:.2%}")
            logger.info(f"🎯 Classification Accuracy: {classification_accuracy:.2%}")
            logger.info(f"💾 Database Accuracy: {database_accuracy:.2%}")
            logger.info(f"⏱️ Duration: {test_duration:.2f} seconds")
            logger.info(f"🏆 Overall Status: {results['overall_status']}")
            
            if results['overall_status'] == "PASSED":
                logger.info("\n🎉 PIPELINE TESTING SUCCESSFUL! System is ready for production!")
            else:
                logger.info("\n⚠️ PIPELINE TESTING REVEALED ISSUES! Review failed tests.")
            
            logger.info("=" * 70)
            
        except Exception as e:
            logger.error(f"❌ Pipeline testing failed: {str(e)}")
            results["error"] = str(e)
            results["overall_status"] = "ERROR"
        
        finally:
            # Cleanup
            self.db.close()
            
        return results

def main():
    """Main pipeline testing entry point"""
    print("🔬 KairoCal Event-to-Priority Pipeline Testing")
    print("=" * 60)
    
    tester = EventPipelineTester()
    results = tester.run_comprehensive_pipeline_test()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"pipeline_test_results_{timestamp}.json"
    
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Test results saved to: {results_file}")
    except Exception as e:
        print(f"⚠️ Failed to save results: {str(e)}")
    
    # Exit with appropriate code
    if results.get("overall_status") == "PASSED":
        print("\n✅ All pipeline tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ Pipeline tests failed: {results.get('error', 'Check results for details')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
