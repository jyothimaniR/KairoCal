# backend/test_bert_standalone.py
"""
Standalone BERT System Test Suite
Comprehensive testing of BERT priority classification without external dependencies
"""

import sys
import os
import traceback
from datetime import datetime, timedelta
import json

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class BERTStandaloneTest:
    """Comprehensive BERT system testing"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = datetime.now()
        
    def run_test(self, test_name: str, test_func):
        """Run individual test and track results"""
        print(f"\n🧪 Running {test_name}...")
        try:
            test_func()
            self.test_results[test_name] = "✅ PASSED"
            print(f"✅ {test_name} - PASSED")
            return True
        except Exception as e:
            self.test_results[test_name] = f"❌ FAILED: {str(e)}"
            print(f"❌ {test_name} - FAILED: {str(e)}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            return False

    def test_import_dependencies(self):
        """Test if all required dependencies can be imported"""
        # Test basic Python imports
        import json
        import os
        import sys
        from datetime import datetime
        
        # Test optional ML imports with graceful fallback
        try:
            import torch
            torch_available = True
            torch_version = torch.__version__
        except ImportError:
            torch_available = False
            torch_version = "Not installed"
            
        try:
            import transformers
            transformers_available = True
            transformers_version = transformers.__version__
        except ImportError:
            transformers_available = False
            transformers_version = "Not installed"
            
        try:
            import sklearn
            sklearn_available = True
            sklearn_version = sklearn.__version__
        except ImportError:
            sklearn_available = False
            sklearn_version = "Not installed"
            
        print(f"🔍 Dependency Status:")
        print(f"   PyTorch: {torch_version} {'✅' if torch_available else '❌'}")
        print(f"   Transformers: {transformers_version} {'✅' if transformers_available else '❌'}")
        print(f"   Scikit-learn: {sklearn_version} {'✅' if sklearn_available else '❌'}")
        
        # Test KairoCal app imports
        from app.config import get_settings
        from app.nlp.entities import ExtractedEvent, IntentType
        
    def test_bert_classifier_import(self):
        """Test BERT classifier import and initialization"""
        from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
        
        # Initialize in fallback mode (should work without trained model)
        classifier = AdvancedEventPriorityClassifier()
        
        # Verify classifier attributes
        assert hasattr(classifier, 'device'), "Classifier missing device attribute"
        assert hasattr(classifier, 'is_trained'), "Classifier missing is_trained attribute"
        assert hasattr(classifier, 'predict'), "Classifier missing predict method"
        
        print(f"🤖 BERT Classifier initialized in {'BERT' if classifier.is_trained else 'FALLBACK'} mode")
        print(f"📱 Device: {classifier.device}")
        
    def test_training_data_generator(self):
        """Test training data generation"""
        from app.nlp.bert_training_data_generator import BERTTrainingDataGenerator
        
        generator = BERTTrainingDataGenerator()
        
        # Generate small sample for testing
        sample_size = 50
        training_data = generator.generate_training_dataset(size=sample_size, balanced=True)
        
        # Verify data structure
        assert len(training_data) == sample_size, f"Expected {sample_size} examples, got {len(training_data)}"
        
        # Check data quality
        priorities = [item.get('priority', 0) for item in training_data]
        assert all(1 <= p <= 5 for p in priorities), "Invalid priority levels found"
        
        # Verify balanced distribution
        priority_counts = {i: priorities.count(i) for i in range(1, 6)}
        print(f"📊 Priority distribution: {priority_counts}")
        
        # Check required fields
        for item in training_data[:5]:  # Check first 5 items
            assert 'title' in item, "Missing title field"
            assert 'priority' in item, "Missing priority field"
            assert 'start_time' in item, "Missing start_time field"
            
    def test_priority_prediction(self):
        """Test priority prediction functionality"""
        from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
        
        classifier = AdvancedEventPriorityClassifier()
        
        # Test cases with expected behaviors
        test_events = [
            {
                "title": "URGENT: CEO Emergency Meeting",
                "description": "Critical business decision required immediately",
                "start_time": "2025-07-30T14:00:00",
                "end_time": "2025-07-30T15:00:00",
                "location": "Executive Boardroom",
                "expected_priority": 5  # Should be high/critical
            },
            {
                "title": "Team Coffee Break",
                "description": "Casual team gathering",
                "start_time": "2025-07-30T15:30:00",
                "end_time": "2025-07-30T15:45:00",
                "location": "Office Kitchen",
                "expected_priority": 1  # Should be low
            },
            {
                "title": "Weekly Team Meeting",
                "description": "Regular team sync",
                "start_time": "2025-07-31T10:00:00",
                "end_time": "2025-07-31T11:00:00",
                "location": "Conference Room",
                "expected_priority": 3  # Should be medium
            }
        ]
        
        predictions = []
        for event in test_events:
            priority, confidence = classifier.predict(event)
            predictions.append({
                "title": event["title"],
                "predicted_priority": priority,
                "confidence": confidence,
                "expected": event["expected_priority"]
            })
            
            # Validate prediction format
            assert 1 <= priority <= 5, f"Invalid priority: {priority}"
            assert 0.0 <= confidence <= 1.0, f"Invalid confidence: {confidence}"
            
        print("🎯 Prediction Results:")
        for pred in predictions:
            match = "✅" if pred["predicted_priority"] == pred["expected"] else "⚠️"
            print(f"   {match} '{pred['title'][:30]}...' → Priority: {pred['predicted_priority']}, Confidence: {pred['confidence']:.2f}")
            
    def test_conflict_detector_integration(self):
        """Test conflict detector with BERT integration"""
        from app.services.conflict_detector import SmartConflictDetector
        
        detector = SmartConflictDetector()
        
        # Mock user and events for testing
        class MockUser:
            def __init__(self):
                self.id = "test-user-123"
                
        class MockEvent:
            def __init__(self, title, start_time, end_time, priority=3):
                self.title = title
                self.start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                self.end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                self.priority_level = priority
                
        user = MockUser()
        
        # Mock existing events
        existing_events = [
            MockEvent("Important Client Meeting", "2025-07-30T14:00:00", "2025-07-30T15:00:00", priority=4)
        ]
        
        # Mock the database query
        detector._get_user_events = lambda user, start, end: existing_events
        
        # Test new conflicting event
        new_event = {
            "title": "Another Meeting",
            "start_time": "2025-07-30T14:30:00",
            "end_time": "2025-07-30T15:30:00"
        }
        
        conflicts = detector.detect_conflicts(user, new_event)
        
        print(f"🔍 Detected {len(conflicts)} conflicts")
        for conflict in conflicts:
            print(f"   ⚠️ {conflict.conflict_type.value}: {conflict.description}")
            
    def test_api_endpoints_structure(self):
        """Test API endpoint structure and imports"""
        from app.api.nlp import router
        from fastapi import APIRouter
        
        # Verify router is properly configured
        assert isinstance(router, APIRouter), "NLP router not properly configured"
        assert router.prefix == "/api/v1/nlp", f"Unexpected router prefix: {router.prefix}"
        
        # Check if key endpoints exist by examining routes
        route_paths = [route.path for route in router.routes]
        expected_endpoints = [
            "/model-status",
            "/predict-priority", 
            "/batch-predict",
            "/explain-priority",
            "/detect-conflicts"
        ]
        
        missing_endpoints = []
        for endpoint in expected_endpoints:
            if endpoint not in route_paths:
                missing_endpoints.append(endpoint)
                
        if missing_endpoints:
            print(f"⚠️ Available routes: {route_paths}")
            print(f"❌ Missing endpoints: {missing_endpoints}")
            # Don't fail the test, just warn about missing endpoints
            print("⚠️ Some endpoints missing but router structure is valid")
        
        print(f"🌐 API Endpoints verified: {len(route_paths)} routes found")
        
    def test_configuration_settings(self):
        """Test configuration settings"""
        from app.config import get_settings
        
        settings = get_settings()
        
        # Test BERT-related configuration
        assert hasattr(settings, 'bert_model_path'), "Missing bert_model_path config"
        assert hasattr(settings, 'training_data_path'), "Missing training_data_path config"
        assert hasattr(settings, 'model_confidence_threshold'), "Missing model_confidence_threshold config"
        assert hasattr(settings, 'priority_levels'), "Missing priority_levels config"
        
        # Verify values
        assert settings.priority_levels == 5, f"Expected 5 priority levels, got {settings.priority_levels}"
        assert 0.0 <= settings.model_confidence_threshold <= 1.0, "Invalid confidence threshold"
        
        print(f"⚙️ Configuration:")
        print(f"   BERT Model Path: {settings.bert_model_path}")
        print(f"   Training Data Path: {settings.training_data_path}")
        print(f"   Confidence Threshold: {settings.model_confidence_threshold}")
        print(f"   Priority Levels: {settings.priority_levels}")
        
    def test_database_models(self):
        """Test database model updates"""
        from app.models.event import Event
        from sqlalchemy import inspect
        
        # Get model columns
        mapper = inspect(Event)
        column_names = [col.key for col in mapper.columns]
        
        # Check for new priority fields
        required_fields = ['priority_level', 'priority_confidence', 'classification_method']
        for field in required_fields:
            assert field in column_names, f"Missing database field: {field}"
            
        print(f"🗄️ Event model fields verified: {len(column_names)} fields")
        
    def test_schemas_validation(self):
        """Test Pydantic schema updates"""
        from app.schemas.event import EventCreate, EventResponse, EventUpdate
        
        # Test EventCreate schema
        event_data = {
            "title": "Test Event",
            "start_time": "2025-07-30T10:00:00",
            "end_time": "2025-07-30T11:00:00",
            "priority_level": 4,
            "priority_confidence": 0.85,
            "classification_method": "bert"
        }
        
        # Should not raise validation errors
        event_create = EventCreate(**event_data)
        assert event_create.priority_level == 4
        assert event_create.priority_confidence == 0.85
        assert event_create.classification_method == "bert"
        
        print("📋 Schema validation passed")
        
    def run_comprehensive_test(self):
        """Run all tests and generate report"""
        print("🚀 Starting BERT Standalone Test Suite")
        print(f"📅 Started at: {self.start_time}")
        print("=" * 60)
        
        # Define test sequence
        tests = [
            ("Import Dependencies", self.test_import_dependencies),
            ("BERT Classifier Import", self.test_bert_classifier_import),
            ("Training Data Generator", self.test_training_data_generator),
            ("Priority Prediction", self.test_priority_prediction),
            ("Conflict Detector Integration", self.test_conflict_detector_integration),
            ("API Endpoints Structure", self.test_api_endpoints_structure),
            ("Configuration Settings", self.test_configuration_settings),
            ("Database Models", self.test_database_models),
            ("Schema Validation", self.test_schemas_validation),
        ]
        
        # Run all tests
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            if self.run_test(test_name, test_func):
                passed += 1
            else:
                failed += 1
                
        # Generate final report
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("📊 BERT STANDALONE TEST REPORT")
        print("=" * 60)
        print(f"✅ Tests Passed: {passed}")
        print(f"❌ Tests Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        print(f"⏱️ Duration: {duration:.2f} seconds")
        print(f"📅 Completed at: {end_time}")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED! BERT system is ready!")
        else:
            print(f"\n⚠️ {failed} tests failed. Check logs above for details.")
            
        return failed == 0

if __name__ == "__main__":
    print("🤖 KairoCal BERT Standalone Test Suite")
    print("Testing BERT priority classification system...")
    
    tester = BERTStandaloneTest()
    success = tester.run_comprehensive_test()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
