# backend/app/tests/test_bert_priority_classifier.py
"""
Comprehensive test suite for BERT Priority Classifier
Tests all components of the BERT-enhanced priority classification system
"""

import pytest
import torch
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import json

from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
from app.nlp.bert_training_data_generator import BERTTrainingDataGenerator
from app.nlp.bert_trainer import BERTPriorityTrainer
from app.services.conflict_detector import SmartConflictDetector

class TestAdvancedEventPriorityClassifier:
    """Test suite for the BERT Priority Classifier"""
    
    @pytest.fixture
    def classifier(self):
        """Create a classifier instance for testing"""
        return AdvancedEventPriorityClassifier()
    
    @pytest.fixture
    def sample_event_data(self):
        """Sample event data for testing"""
        return {
            "title": "Important Client Meeting",
            "description": "Quarterly review with major client",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
            "location": "Conference Room A"
        }
    
    def test_classifier_initialization(self, classifier):
        """Test that classifier initializes correctly"""
        assert classifier is not None
        assert classifier.device is not None
        assert classifier.tokenizer is not None
        assert len(classifier.priority_labels) == 5
        assert not classifier.is_trained  # Should be False for new instance
    
    def test_temporal_feature_extraction(self, classifier, sample_event_data):
        """Test temporal feature extraction"""
        features = classifier._extract_temporal_features(sample_event_data)
        
        assert isinstance(features, np.ndarray)
        assert len(features) == 8  # Expected number of temporal features
        assert all(-1 <= f <= 1 for f in features[:4])  # Cyclical features should be normalized
    
    def test_location_feature_extraction(self, classifier):
        """Test location feature extraction"""
        # Test office location
        office_features = classifier._extract_location_features("Conference Room A")
        assert len(office_features) == 8
        assert office_features[0] == 1.0  # Should detect office
        
        # Test remote location
        remote_features = classifier._extract_location_features("Zoom Meeting")
        assert remote_features[7] == 1.0  # Should detect remote
        
        # Test no location
        no_location_features = classifier._extract_location_features(None)
        assert all(f == 0.0 for f in no_location_features)
    
    def test_content_feature_extraction(self, classifier, sample_event_data):
        """Test content feature extraction"""
        features = classifier._extract_content_features(sample_event_data)
        
        assert isinstance(features, np.ndarray)
        assert len(features) == 8
        
        # Test urgency detection
        urgent_event = {
            "title": "URGENT: System Down",
            "description": "Critical emergency response needed"
        }
        urgent_features = classifier._extract_content_features(urgent_event)
        assert urgent_features[1] == 1.0  # Should detect urgency
    
    def test_fallback_priority_classification(self, classifier):
        """Test fallback priority classification when BERT is not available"""
        # Test critical priority
        critical_event = {
            "title": "URGENT CEO Meeting",
            "description": "Critical emergency situation"
        }
        priority, confidence = classifier._fallback_priority_classification(critical_event)
        assert priority == 5
        assert confidence > 0.5
        
        # Test low priority
        low_event = {
            "title": "Coffee Break",
            "description": "Casual break time"
        }
        priority, confidence = classifier._fallback_priority_classification(low_event)
        assert priority == 1
        assert confidence > 0.3
    
    def test_predict_with_fallback(self, classifier, sample_event_data):
        """Test prediction with fallback (when BERT is not trained)"""
        priority, confidence = classifier.predict(sample_event_data)
        
        assert 1 <= priority <= 5
        assert 0 <= confidence <= 1
        assert isinstance(priority, int)
        assert isinstance(confidence, float)
    
    def test_explain_prediction(self, classifier, sample_event_data):
        """Test prediction explanation"""
        explanation = classifier.explain_prediction(sample_event_data)
        
        assert "priority" in explanation
        assert "priority_label" in explanation
        assert "confidence" in explanation
        assert "reasoning" in explanation
        
        assert 1 <= explanation["priority"] <= 5
        assert explanation["priority_label"] in classifier.priority_labels.values()

class TestBERTTrainingDataGenerator:
    """Test suite for the training data generator"""
    
    @pytest.fixture
    def generator(self):
        """Create a data generator instance"""
        return BERTTrainingDataGenerator()
    
    def test_generator_initialization(self, generator):
        """Test that generator initializes with proper templates"""
        assert len(generator.priority_templates) == 5
        assert len(generator.locations) > 0
        assert len(generator.time_patterns) > 0
        
        # Check that all priority levels have templates
        for priority in range(1, 6):
            assert priority in generator.priority_templates
            assert len(generator.priority_templates[priority][0]["title_templates"]) > 0
    
    def test_generate_single_training_example(self, generator):
        """Test generation of a single training example"""
        example = generator.generate_training_example(priority=3)
        
        assert "title" in example
        assert "description" in example
        assert "start_time" in example
        assert "end_time" in example
        assert "priority" in example
        assert example["priority"] == 3
        
        # Validate time format
        start_time = datetime.fromisoformat(example["start_time"])
        end_time = datetime.fromisoformat(example["end_time"])
        assert end_time > start_time
    
    def test_generate_training_dataset_balanced(self, generator):
        """Test balanced dataset generation"""
        dataset = generator.generate_training_dataset(size=100, balanced=True)
        
        assert len(dataset) == 100
        
        # Check priority distribution
        priority_counts = {}
        for example in dataset:
            priority = example["priority"]
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Should be roughly equal distribution
        for priority in range(1, 6):
            assert priority in priority_counts
            assert 15 <= priority_counts[priority] <= 25  # Allow some variance
    
    def test_generate_validation_scenarios(self, generator):
        """Test validation scenario generation"""
        scenarios = generator.generate_validation_scenarios()
        
        assert len(scenarios) > 0
        
        for scenario in scenarios:
            assert "title" in scenario
            assert "expected_priority" in scenario
            assert 1 <= scenario["expected_priority"] <= 5
    
    def test_dataset_analysis(self, generator):
        """Test dataset analysis functionality"""
        dataset = generator.generate_training_dataset(size=50)
        analysis = generator.analyze_dataset(dataset)
        
        assert "total_examples" in analysis
        assert "priority_distribution" in analysis
        assert "location_distribution" in analysis
        assert "time_distribution" in analysis
        assert analysis["total_examples"] == 50

class TestSmartConflictDetectorWithBERT:
    """Test suite for conflict detector with BERT integration"""
    
    @pytest.fixture
    def conflict_detector(self):
        """Create a conflict detector instance"""
        return SmartConflictDetector()
    
    @pytest.fixture
    def mock_user(self):
        """Create a mock user object"""
        user = Mock()
        user.id = "test_user_123"
        return user
    
    def test_conflict_detector_initialization(self, conflict_detector):
        """Test that conflict detector initializes correctly"""
        assert conflict_detector is not None
        # Should handle cases where BERT is not available gracefully
    
    def test_enhanced_priority_inference(self, conflict_detector):
        """Test enhanced priority inference"""
        event_data = {
            "title": "CRITICAL: System Outage",
            "description": "Emergency response required",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        priority, confidence = conflict_detector._infer_event_priority_enhanced(event_data)
        
        assert 1 <= priority <= 5
        assert 0 <= confidence <= 1
        assert priority >= 4  # Should be high priority for critical event
    
    def test_priority_conflict_detection(self, conflict_detector, mock_user):
        """Test priority-based conflict detection"""
        # Mock existing event
        existing_event = Mock()
        existing_event.title = "Team Meeting"
        existing_event.description = "Regular weekly sync"
        existing_event.start_time = datetime.now()
        existing_event.end_time = datetime.now() + timedelta(hours=1)
        existing_event.location = "Conference Room"
        existing_event.id = "existing_event_123"
        
        new_event_data = {
            "title": "URGENT: CEO Emergency Meeting",
            "description": "Critical business decision required",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        conflicts = conflict_detector._detect_priority_conflicts(
            existing_event, 
            new_event_data, 
            new_event_priority=5,
            priority_confidence=0.9,
            user_context={}
        )
        
        # Should detect priority conflict (high priority vs medium priority)
        assert len(conflicts) > 0
        conflict = conflicts[0]
        assert conflict.conflict_type.value == "priority_conflict"
        assert len(conflict.suggested_resolutions) > 0
    
    def test_explain_priority_decision(self, conflict_detector):
        """Test priority decision explanation"""
        event_data = {
            "title": "Important Client Presentation",
            "description": "Quarterly business review",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=2)).isoformat()
        }
        
        explanation = conflict_detector.explain_priority_decision(event_data)
        
        assert "priority" in explanation
        assert "priority_label" in explanation
        assert "confidence" in explanation
        assert "reasoning" in explanation

class TestAPIIntegration:
    """Test suite for API integration"""
    
    def test_api_endpoints_exist(self):
        """Test that required API endpoints are available"""
        from app.api.nlp import router
        
        # Check that router exists and has expected routes
        routes = [route.path for route in router.routes]
        
        expected_routes = [
            "/api/v1/nlp/predict-priority",
            "/api/v1/nlp/explain-priority",
            "/api/v1/nlp/batch-predict",
            "/api/v1/nlp/model-status"
        ]
        
        for expected_route in expected_routes:
            assert any(expected_route in route for route in routes)

class TestPerformanceAndRobustness:
    """Test suite for performance and robustness"""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier for performance testing"""
        return AdvancedEventPriorityClassifier()
    
    def test_prediction_performance(self, classifier):
        """Test that predictions complete within reasonable time"""
        import time
        
        event_data = {
            "title": "Test Event",
            "description": "Test description",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        start_time = time.time()
        priority, confidence = classifier.predict(event_data)
        end_time = time.time()
        
        # Should complete within 1 second (generous for fallback mode)
        assert (end_time - start_time) < 1.0
        assert 1 <= priority <= 5
    
    def test_batch_prediction_performance(self, classifier):
        """Test batch prediction performance"""
        import time
        
        # Generate multiple events
        events = []
        for i in range(10):
            events.append({
                "title": f"Test Event {i}",
                "description": f"Test description {i}",
                "start_time": (datetime.now() + timedelta(hours=i)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=i+1)).isoformat()
            })
        
        start_time = time.time()
        predictions = []
        for event in events:
            priority, confidence = classifier.predict(event)
            predictions.append((priority, confidence))
        end_time = time.time()
        
        # Should complete batch processing efficiently
        assert len(predictions) == 10
        assert (end_time - start_time) < 5.0  # 5 seconds for 10 predictions
    
    def test_edge_cases_robustness(self, classifier):
        """Test robustness with edge cases"""
        edge_cases = [
            # Empty strings
            {"title": "", "description": "", "start_time": datetime.now().isoformat(), "end_time": (datetime.now() + timedelta(hours=1)).isoformat()},
            # Very long strings
            {"title": "A" * 1000, "description": "B" * 2000, "start_time": datetime.now().isoformat(), "end_time": (datetime.now() + timedelta(hours=1)).isoformat()},
            # Special characters
            {"title": "Meeting @#$%^&*()", "description": "Special chars: ñáéíóú", "start_time": datetime.now().isoformat(), "end_time": (datetime.now() + timedelta(hours=1)).isoformat()},
            # Invalid dates (should be handled gracefully)
            {"title": "Test", "description": "Test", "start_time": "invalid_date", "end_time": "also_invalid"}
        ]
        
        for event_data in edge_cases:
            try:
                priority, confidence = classifier.predict(event_data)
                assert 1 <= priority <= 5
                assert 0 <= confidence <= 1
            except Exception as e:
                # Should handle gracefully, not crash
                pytest.fail(f"Classifier failed on edge case: {event_data}, error: {e}")

# Performance benchmarks
@pytest.mark.benchmark
class TestBenchmarks:
    """Benchmark tests for performance measurement"""
    
    def test_single_prediction_benchmark(self, benchmark):
        """Benchmark single prediction performance"""
        classifier = AdvancedEventPriorityClassifier()
        
        event_data = {
            "title": "Important Meeting",
            "description": "Strategic planning session",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=2)).isoformat()
        }
        
        def predict():
            return classifier.predict(event_data)
        
        result = benchmark(predict)
        priority, confidence = result
        assert 1 <= priority <= 5
    
    def test_feature_extraction_benchmark(self, benchmark):
        """Benchmark feature extraction performance"""
        classifier = AdvancedEventPriorityClassifier()
        
        event_data = {
            "title": "Complex Event Title with Many Words and Details",
            "description": "This is a very detailed description with lots of information about the event including location context and temporal details",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
            "location": "Main Conference Room, Building A, Floor 3"
        }
        
        def extract_features():
            return classifier._combine_features(event_data)
        
        result = benchmark(extract_features)
        text_features, other_features = result
        assert text_features is not None
        assert other_features is not None

# Integration tests
class TestEndToEndIntegration:
    """End-to-end integration tests"""
    
    def test_training_to_prediction_pipeline(self):
        """Test complete pipeline from training data generation to prediction"""
        # 1. Generate training data
        generator = BERTTrainingDataGenerator()
        training_data = generator.generate_training_dataset(size=20, balanced=True)
        
        # 2. Initialize classifier
        classifier = AdvancedEventPriorityClassifier()
        
        # 3. Test prediction (will use fallback since not trained)
        test_event = training_data[0]
        priority, confidence = classifier.predict(test_event)
        
        assert 1 <= priority <= 5
        assert 0 <= confidence <= 1
    
    def test_conflict_detection_integration(self):
        """Test integration between BERT classifier and conflict detection"""
        # Initialize components
        conflict_detector = SmartConflictDetector()
        
        # Create test event
        event_data = {
            "title": "URGENT: Critical System Review",
            "description": "Emergency assessment of system failures",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=2)).isoformat()
        }
        
        # Test priority explanation
        explanation = conflict_detector.explain_priority_decision(event_data)
        
        assert explanation["priority"] >= 4  # Should be high priority
        assert "reasoning" in explanation

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])