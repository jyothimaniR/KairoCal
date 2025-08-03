#!/usr/bin/env python3
"""
Simple BERT Integration Test
"""

import sys
import os
import logging

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_imports():
    """Test basic system imports"""
    print("🔍 Testing Basic Imports")
    
    try:
        from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
        print("✅ BERT Classifier imported")
    except Exception as e:
        print(f"❌ BERT Classifier import failed: {e}")
        return False
    
    try:
        from app.nlp.model_loader import get_global_bert_model
        print("✅ Model Loader imported")
    except Exception as e:
        print(f"❌ Model Loader import failed: {e}")
        return False
    
    return True

def test_bert_model_loading():
    """Test BERT model loading"""
    print("\n🤖 Testing BERT Model Loading")
    
    try:
        from app.nlp.model_loader import get_global_bert_model
        model = get_global_bert_model()
        
        print(f"Model loaded: {model is not None}")
        print(f"Model trained: {model.is_trained}")
        
        return True
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_prediction():
    """Test model prediction"""
    print("\n📊 Testing Model Prediction")
    
    try:
        from app.nlp.model_loader import get_global_bert_model
        model = get_global_bert_model()
        
        test_event = {
            "title": "Important meeting tomorrow",
            "description": "Critical business meeting with stakeholders",
            "start_time": "2025-08-02T10:00:00",
            "location": "Conference Room"
        }
        
        priority, confidence = model.predict(test_event)
        print(f"Prediction: Priority {priority}, Confidence {confidence:.3f}")
        
        return True
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🧪 Simple BERT Integration Test")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Model Loading", test_bert_model_loading),
        ("Prediction", test_prediction)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System integration working.")
        return True
    else:
        print("⚠️ Some tests failed. Check system components.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
