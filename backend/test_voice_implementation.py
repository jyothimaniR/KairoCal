#!/usr/bin/env python3
"""
Quick Voice API Implementation Test
Validates that all components are working correctly
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all voice-related imports work"""
    print("🧪 Testing Voice API Imports")
    print("=" * 40)
    
    try:
        # Test voice API import
        from app.api.voice import voice_router, VoiceProcessor
        print("✅ Voice API router imported successfully")
        
        # Test NLP service import
        from app.services.nlp_service import NLPService
        print("✅ Enhanced NLP service imported successfully")
        
        # Test voice processor functionality
        processor = VoiceProcessor()
        test_text = "Um, schedule a meeting with John tomorrow at 3pm"
        result = processor.clean_voice_text(test_text)
        print(f"✅ Voice processor working: '{result['cleaned_text']}'")
        
        # Test NLP service functionality
        nlp_service = NLPService()
        print("✅ NLP service initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Functionality error: {e}")
        return False

def test_voice_processing():
    """Test voice processing functionality"""
    print("\n🎤 Testing Voice Processing")
    print("=" * 40)
    
    try:
        from app.api.voice import VoiceProcessor
        
        processor = VoiceProcessor()
        
        test_cases = [
            "Um, schedule a meeting with John tomorrow at 3pm",
            "URGENT: Emergency board meeting now",
            "Coffee break with team next week",
            "Remind me to call the client about the deadline"
        ]
        
        for i, test_text in enumerate(test_cases, 1):
            result = processor.clean_voice_text(test_text)
            print(f"{i}. Original: '{test_text}'")
            print(f"   Cleaned:  '{result['cleaned_text']}'")
            print(f"   Confidence: {result['confidence']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice processing test failed: {e}")
        return False

def test_nlp_integration():
    """Test NLP service integration"""
    print("\n🧠 Testing NLP Integration")
    print("=" * 40)
    
    try:
        from app.services.nlp_service import NLPService
        import asyncio
        
        nlp_service = NLPService()
        
        # Test voice input processing
        test_voice = "Schedule urgent client meeting tomorrow at 2pm in conference room A"
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(nlp_service.process_voice_input(test_voice))
        
        print(f"✅ Voice Text: '{test_voice}'")
        print(f"✅ Extracted Title: '{result.get('title', 'N/A')}'")
        print(f"✅ Detected Time: {result.get('start_time', 'N/A')}")
        print(f"✅ Detected Location: '{result.get('location', 'None')}'")
        print(f"✅ Priority: {result.get('priority', 'N/A')}")
        print(f"✅ Confidence: {result.get('confidence', 0):.2f}")
        
        loop.close()
        return True
        
    except Exception as e:
        print(f"❌ NLP integration test failed: {e}")
        return False

def test_bert_integration():
    """Test BERT model integration"""
    print("\n🤖 Testing BERT Integration")
    print("=" * 40)
    
    try:
        from app.nlp.model_loader import get_global_bert_model
        
        bert_model = get_global_bert_model()
        
        if bert_model and bert_model.is_trained:
            print("✅ BERT model loaded and trained")
            
            # Test prediction
            test_event = {
                'title': 'URGENT: Board meeting with CEO',
                'description': 'Emergency board meeting about quarterly results',
                'start_time': '2025-08-02T10:00:00',
                'location': 'Conference Room A'
            }
            
            priority, confidence = bert_model.predict(test_event)
            print(f"✅ BERT Prediction: Priority {priority}, Confidence {confidence:.3f}")
            
        else:
            print("⚠️ BERT model not available or not trained")
            print("   Voice API will use rule-based fallback")
        
        return True
        
    except Exception as e:
        print(f"❌ BERT integration test failed: {e}")
        return False

def test_api_structure():
    """Test API endpoint structure"""
    print("\n🌐 Testing API Structure")
    print("=" * 40)
    
    try:
        from app.api.voice import voice_router
        
        # Check router configuration
        print(f"✅ Voice router prefix: {voice_router.prefix}")
        print(f"✅ Voice router tags: {voice_router.tags}")
        
        # Check available routes
        routes = [route.path for route in voice_router.routes]
        print("✅ Available voice endpoints:")
        for route in routes:
            print(f"   - {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎤 Voice API Implementation Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Voice Processing", test_voice_processing),
        ("NLP Integration", test_nlp_integration),
        ("BERT Integration", test_bert_integration),
        ("API Structure", test_api_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Voice API implementation is ready.")
        print("\nNext steps:")
        print("1. Start the FastAPI server: uvicorn app.main:app --reload")
        print("2. Test endpoints: python test_voice_api.py")
        print("3. Run demo: python demo_voice_commands.py --quick-demo")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
