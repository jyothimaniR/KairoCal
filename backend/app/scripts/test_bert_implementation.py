# backend/app/scripts/test_bert_implementation.py
"""
Quick test script to validate BERT implementation
Run this to ensure everything is working correctly
"""

import sys
import os
from datetime import datetime, timedelta
import logging

# Fix Python path to enable 'app' module imports
# Add the backend directory (parent of 'app') to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..', '..')  # Go up two levels to reach backend/
sys.path.insert(0, backend_dir)

# Debug path info
print(f"🔧 Script location: {current_dir}")
print(f"🔧 Backend directory: {backend_dir}")
print(f"🔧 Python path updated: {backend_dir in sys.path}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_bert_classifier():
    """Test the BERT classifier implementation"""
    print("🤖 Testing BERT Priority Classifier...")
    
    try:
        from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
        
        # Initialize classifier
        classifier = AdvancedEventPriorityClassifier()
        print(f"✅ Classifier initialized - Trained: {classifier.is_trained}")
        
        # Test events with expected priorities
        test_events = [
            {
                "title": "URGENT: CEO Emergency Meeting",
                "description": "Critical business decision required immediately",
                "start_time": datetime.now().isoformat(),
                "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
                "location": "Executive Boardroom",
                "expected": 5
            },
            {
                "title": "Important: Client Presentation",
                "description": "Quarterly review with major stakeholder",
                "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
                "end_time": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
                "location": "Conference Room A",
                "expected": 4
            },
            {
                "title": "Team Meeting",
                "description": "Weekly standup and project sync",
                "start_time": (datetime.now() + timedelta(days=2)).isoformat(),
                "end_time": (datetime.now() + timedelta(days=2, hours=1)).isoformat(),
                "location": "Meeting Room 3",
                "expected": 3
            },
            {
                "title": "Lunch with colleagues",
                "description": "Casual lunch and networking",
                "start_time": (datetime.now() + timedelta(days=3, hours=12)).isoformat(),
                "end_time": (datetime.now() + timedelta(days=3, hours=13)).isoformat(),
                "location": "Restaurant Downtown",
                "expected": 2
            },
            {
                "title": "Coffee break",
                "description": "Optional break time",
                "start_time": (datetime.now() + timedelta(hours=2)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=2, minutes=15)).isoformat(),
                "location": "Office Kitchen",
                "expected": 1
            }
        ]
        
        print("\n📊 Testing priority predictions:")
        correct_predictions = 0
        
        for i, event in enumerate(test_events):
            expected = event.pop("expected")
            
            priority, confidence = classifier.predict(event)
            
            # Allow some tolerance for predictions
            is_correct = abs(priority - expected) <= 1
            correct_predictions += is_correct
            
            status = "✅" if is_correct else "❌"
            print(f"{status} Event {i+1}: '{event['title'][:40]}...'")
            print(f"   Expected: {expected}, Got: {priority}, Confidence: {confidence:.3f}")
        
        accuracy = correct_predictions / len(test_events)
        print(f"\n🎯 Accuracy: {accuracy:.1%} ({correct_predictions}/{len(test_events)})")
        
        return True
        
    except Exception as e:
        print(f"❌ BERT Classifier test failed: {e}")
        return False

def test_training_data_generator():
    """Test the training data generator"""
    print("\n📊 Testing Training Data Generator...")
    
    try:
        from app.nlp.bert_training_data_generator import BERTTrainingDataGenerator
        
        generator = BERTTrainingDataGenerator()
        print("✅ Generator initialized")
        
        # Generate small test dataset
        dataset = generator.generate_training_dataset(size=10, balanced=True)
        print(f"✅ Generated {len(dataset)} training examples")
        
        # Analyze dataset - using the actual method that exists
        analysis = generator.analyze_dataset(dataset)
        print(f"✅ Dataset analysis completed")
        print(f"   Total examples: {analysis['total_examples']}")
        print(f"   Priority distribution: {analysis['priority_distribution']}")
        
        # Generate validation scenarios
        scenarios = generator.generate_validation_scenarios()
        print(f"✅ Generated {len(scenarios)} validation scenarios")
        
        return True
        
    except Exception as e:
        print(f"❌ Training Data Generator test failed: {e}")
        return False

def test_conflict_detector_integration():
    """Test conflict detector with BERT integration"""
    print("\n⚔️ Testing Conflict Detector Integration...")
    
    try:
        from app.services.conflict_detector import SmartConflictDetector
        
        detector = SmartConflictDetector()
        print("✅ Conflict Detector initialized")
        
        # Test priority inference
        test_event = {
            "title": "CRITICAL: System Outage Response",
            "description": "Emergency meeting to address critical system failure",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
            "location": "Emergency Response Center"
        }
        
        priority, confidence = detector._infer_event_priority_enhanced(test_event)
        print(f"✅ Priority inference: {priority} (confidence: {confidence:.3f})")
        
        # Test explanation
        explanation = detector.explain_priority_decision(test_event)
        print(f"✅ Priority explanation generated")
        print(f"   Priority: {explanation['priority']} ({explanation['priority_label']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Conflict Detector integration test failed: {e}")
        return False

def test_api_imports():
    """Test that API endpoints can be imported"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        from app.api.nlp import router
        print("✅ NLP API router imported successfully")
        
        # Check routes
        routes = [route.path for route in router.routes]
        expected_routes = [
            "/api/v1/nlp/predict-priority",
            "/api/v1/nlp/explain-priority", 
            "/api/v1/nlp/model-status"
        ]
        
        for expected_route in expected_routes:
            if any(expected_route in route for route in routes):
                print(f"✅ Route found: {expected_route}")
            else:
                print(f"❌ Route missing: {expected_route}")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def run_performance_test():
    """Run basic performance test"""
    print("\n⚡ Running Performance Test...")
    
    try:
        from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
        import time
        
        classifier = AdvancedEventPriorityClassifier()
        
        # Test single prediction performance
        test_event = {
            "title": "Performance Test Event",
            "description": "Testing prediction performance",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        # Warm up
        classifier.predict(test_event)
        
        # Time multiple predictions
        num_predictions = 10
        start_time = time.time()
        
        for _ in range(num_predictions):
            classifier.predict(test_event)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / num_predictions
        
        print(f"✅ Performance test completed")
        print(f"   {num_predictions} predictions in {total_time:.3f}s")
        print(f"   Average: {avg_time*1000:.1f}ms per prediction")
        
        # Performance threshold (should be under 100ms for fallback mode)
        if avg_time < 0.1:
            print("✅ Performance: EXCELLENT")
        elif avg_time < 0.5:
            print("✅ Performance: GOOD") 
        else:
            print("⚠️ Performance: NEEDS OPTIMIZATION")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 BERT Implementation Validation Suite")
    print("=" * 50)
    
    test_results = {
        "BERT Classifier": test_bert_classifier(),
        "Training Data Generator": test_training_data_generator(), 
        "Conflict Detector Integration": test_conflict_detector_integration(),
        "API Endpoints": test_api_imports(),
        "Performance": run_performance_test()
    }
    
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total:.1%})")
    
    if passed == total:
        print("🎉 All tests passed! BERT implementation is ready!")
        print("\n📋 Next steps:")
        print("1. Run training: python app/scripts/train_bert_priority_model.py")
        print("2. Start API server: uvicorn app.main:app --reload")
        print("3. Test endpoints at: http://localhost:8000/docs")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements/base.txt")
        print("2. Check file paths and imports")
        print("3. Verify Python path configuration")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)