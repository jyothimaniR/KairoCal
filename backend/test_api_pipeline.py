#!/usr/bin/env python3
"""
Test script to simulate the exact API call the frontend makes
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the request classes from the voice API
class MockVoiceCreateEventRequest:
    def __init__(self, voice_text, user_id, auto_schedule=True, priority_override=None, duration_preference=None):
        self.voice_text = voice_text
        self.user_id = user_id  
        self.auto_schedule = auto_schedule
        self.priority_override = priority_override
        self.duration_preference = duration_preference

async def test_voice_api_logic():
    """Test the voice API logic that creates events"""
    
    # Import the voice processing logic
    from app.api.voice import VoiceProcessor
    from app.services.nlp_service import NLPService
    
    print("🎤 TESTING VOICE API PIPELINE")
    print("=" * 60)
    
    # Test input from the screenshot
    test_input = "Play Football With Friends Coming At The Anfield Stadium"
    print(f"Input: '{test_input}'")
    print()
    
    # Step 1: Voice Processing (like the API does)
    processor = VoiceProcessor()
    cleaning_result = processor.clean_voice_text(test_input)
    cleaned_text = cleaning_result['cleaned_text']
    
    print(f"🧹 Cleaned text: '{cleaned_text}'")
    print()
    
    # Step 2: NLP Processing (like the API does)
    nlp_service = NLPService()
    nlp_result = await nlp_service.process_voice_input(cleaned_text, None)
    
    print("📊 NLP RESULT:")
    print(f"  Title: '{nlp_result.get('title', 'None')}'")
    print(f"  Location: '{nlp_result.get('location', 'None')}'")
    print(f"  Description: '{nlp_result.get('description', 'None')}'")
    print(f"  Priority: {nlp_result.get('priority', 'None')}")
    print(f"  Start Time: {nlp_result.get('start_time', 'None')}")
    print(f"  End Time: {nlp_result.get('end_time', 'None')}")
    print()
    
    # Step 3: Check what would be stored in the database
    title_for_db = nlp_result.get('title', 'Voice Event')
    location_for_db = nlp_result.get('location', '')
    
    print("💾 DATABASE VALUES:")
    print(f"  Title to store: '{title_for_db}'")
    print(f"  Location to store: '{location_for_db}'")
    print()
    
    # Test if there are any overrides happening
    if title_for_db != nlp_result.get('title'):
        print("⚠️ WARNING: Title is being modified after NLP processing!")
    
    if location_for_db != nlp_result.get('location'):
        print("⚠️ WARNING: Location is being modified after NLP processing!")

if __name__ == "__main__":
    asyncio.run(test_voice_api_logic())
