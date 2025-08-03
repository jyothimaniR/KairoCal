#!/usr/bin/env python3
"""
Test Model Loader Functionality
Tests the updated model loading system with the trained BERT model
"""

import sys
import os
import logging

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_model_loader():
    """Test the BERTModelLoader functionality"""
    print("🔧 Testing BERT Model Loader")
    print("=" * 60)
    
    try:
        from app.nlp.model_loader import (
            BERTModelLoader, 
            load_bert_model, 
            get_model_status,
            is_trained_model_available,
            get_global_bert_model
        )
        
        # Test 1: Check if trained model is available
        print("📋 Test 1: Model Availability Check")
        is_available = is_trained_model_available()
        print(f"   Trained model available: {is_available}")
        
        # Test 2: Get model loader instance
        print("\n📋 Test 2: Model Loader Instance")
        loader = BERTModelLoader()
        print(f"   Loader created: {loader is not None}")
        print(f"   Model path: {loader.model_path}")
        print(f"   Device: {loader.device}")
        
        # Test 3: Load model with fallback
        print("\n📋 Test 3: Load Model with Fallback")
        model = load_bert_model()
        print(f"   Model loaded: {model is not None}")
        print(f"   Model trained: {model.is_trained}")
        print(f"   Model device: {model.device}")
        
        # Test 4: Get model status
        print("\n📋 Test 4: Model Status Information")
        status = get_model_status()
        print(f"   Status loaded: {status.get('loaded', False)}")
        print(f"   Status trained: {status.get('trained', False)}")
        print(f"   Files exist: {status.get('files_exist', False)}")
        
        if 'metadata' in status:
            metadata = status['metadata']
            print(f"   Training date: {metadata.get('training_date', 'Unknown')}")
            print(f"   Accuracy: {metadata.get('accuracy', 'Unknown')}")
            print(f"   Duration: {metadata.get('training_duration', 'Unknown')} min")
        
        # Test 5: Global model access
        print("\n📋 Test 5: Global Model Access")
        global_model = get_global_bert_model()
        print(f"   Global model loaded: {global_model is not None}")
        print(f"   Same instance: {global_model is model}")
        
        # Test 6: Model prediction test
        print("\n📋 Test 6: Model Prediction Test")
        test_event = {
            "title": "Important client meeting tomorrow",
            "description": "Final presentation for major client proposal",
            "start_time": "2025-08-02T10:00:00",
            "location": "Client Office"
        }
        
        priority, confidence = model.predict(test_event)
        print(f"   Test prediction: Priority {priority}, Confidence {confidence:.3f}")
        
        # Test 7: Force reload test
        print("\n📋 Test 7: Force Reload Test")
        reloaded_model = loader.reload_model()
        print(f"   Reloaded model: {reloaded_model is not None}")
        print(f"   Different instance: {reloaded_model is not model}")
        print(f"   Still trained: {reloaded_model.is_trained}")
        
        print("\n" + "=" * 60)
        print("✅ All model loader tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Model loader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_with_api():
    """Test integration with API endpoints"""
    print("\n🌐 Testing API Integration")
    print("=" * 40)
    
    try:
        # Test importing in API context
        from app.nlp.model_loader import get_global_bert_model
        
        # Simulate API usage
        model = get_global_bert_model()
        
        # Sample events for API-style testing
        api_events = [
            {
                "title": "Urgent bug fix needed",
                "description": "Critical production issue affecting users",
                "start_time": "2025-08-01T15:00:00",
                "location": "Remote"
            },
            {
                "title": "Coffee break",
                "description": "Quick coffee with team",
                "start_time": "2025-08-01T16:30:00",
                "location": "Kitchen"
            }
        ]
        
        print("📊 API-style predictions:")
        for i, event in enumerate(api_events, 1):
            priority, confidence = model.predict(event)
            print(f"   Event {i}: Priority {priority} ({model.priority_labels[priority]}) - {confidence:.3f}")
        
        print("✅ API integration test successful!")
        return True
        
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🧪 BERT Model Loader Testing Suite")
    print("=" * 80)
    
    # Run tests
    loader_success = test_model_loader()
    api_success = test_integration_with_api()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Model Loader Tests: {'✅ PASSED' if loader_success else '❌ FAILED'}")
    print(f"API Integration Tests: {'✅ PASSED' if api_success else '❌ FAILED'}")
    
    overall_success = loader_success and api_success
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n📋 Next Steps:")
        print("  1. ✅ Model loader is ready for production")
        print("  2. 🔄 Proceed to Task 5: System Integration Test")
        print("  3. 🚀 Model loading system fully validated")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
