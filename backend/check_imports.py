#!/usr/bin/env python3
"""
Check which NLP service is actually being imported by the voice API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_nlp_imports():
    try:
        print("🔍 CHECKING NLP SERVICE IMPORTS")
        print("=" * 60)
        
        # Test import from voice API
        from app.api.voice import NLPService as VoiceNLPService
        print(f"✅ Voice API imports NLPService from: {VoiceNLPService.__module__}")
        print(f"   File: {VoiceNLPService.__module__.replace('.', '/')}.py")
        print()
        
        # Test the actual methods
        voice_nlp = VoiceNLPService()
        
        # Check if it has the methods I fixed
        has_extract_title = hasattr(voice_nlp, '_extract_title')
        has_extract_location = hasattr(voice_nlp, '_extract_location')
        has_process_voice_input = hasattr(voice_nlp, 'process_voice_input')
        
        print(f"🔧 Methods available:")
        print(f"   _extract_title: {has_extract_title}")
        print(f"   _extract_location: {has_extract_location}")
        print(f"   process_voice_input: {has_process_voice_input}")
        print()
        
        # Test the specific methods I fixed
        if has_extract_title:
            test_input = "Coffee With Friends At The Liverpool Cafe Coming"
            title_result = voice_nlp._extract_title(test_input)
            print(f"🧪 _extract_title('{test_input}'):")
            print(f"   Result: '{title_result}'")
            print()
        
        if has_extract_location:
            location_result = voice_nlp._extract_location(test_input)
            print(f"🧪 _extract_location('{test_input}'):")
            print(f"   Result: '{location_result}'")
            print()
        
        # Check if there are other NLP services
        print("🔍 Checking other NLP services:")
        try:
            from app.nlp.nlp_service import NLPService as NlpNLPService
            print(f"✅ app.nlp.nlp_service exists: {NlpNLPService.__module__}")
        except ImportError as e:
            print(f"❌ app.nlp.nlp_service import failed: {e}")
        
        try:
            from app.services.nlp_service import NLPService as ServicesNLPService
            print(f"✅ app.services.nlp_service exists: {ServicesNLPService.__module__}")
        except ImportError as e:
            print(f"❌ app.services.nlp_service import failed: {e}")
        
    except Exception as e:
        print(f"❌ Import check failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_nlp_imports()
