#!/usr/bin/env python3
"""
Debug script to trace the exact voice event creation flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import json
from unittest.mock import Mock

async def test_voice_api_endpoint():
    """Test the exact API endpoint that the frontend calls"""
    
    print("🔍 TESTING VOICE API ENDPOINT")
    print("=" * 60)
    
    # Import the voice API function directly
    from app.api.voice import create_event_from_voice, VoiceCreateEventRequest
    from app.core.database import get_db
    
    # Create a mock request like the frontend sends
    test_request = VoiceCreateEventRequest(
        voice_text="Coffee With Friends At The Liverpool Cafe Coming",
        user_id="550e8400-e29b-41d4-a716-446655440000",  # Use a test UUID
        auto_schedule=True,
        priority_override=None,
        duration_preference="smart"
    )
    
    print(f"📤 Request:")
    print(f"  voice_text: '{test_request.voice_text}'")
    print(f"  user_id: {test_request.user_id}")
    print(f"  auto_schedule: {test_request.auto_schedule}")
    print(f"  duration_preference: {test_request.duration_preference}")
    print()
    
    # Mock database session
    db_mock = Mock()
    
    try:
        # Call the actual API function
        response = await create_event_from_voice(test_request, db_mock)
        
        print("📥 Response:")
        print(f"  success: {response.success}")
        print(f"  event_id: {response.event_id}")
        print(f"  message: {response.message}")
        print()
        
        print("📊 NLP Analysis:")
        nlp_analysis = response.nlp_analysis
        print(f"  original_text: '{nlp_analysis.get('original_text', 'None')}'")
        print(f"  cleaned_text: '{nlp_analysis.get('cleaned_text', 'None')}'")
        print(f"  extracted_title: '{nlp_analysis.get('extracted_title', 'None')}'")
        print(f"  extracted_location: '{nlp_analysis.get('extracted_location', 'None')}'")
        print()
        
        print("💾 Event Data:")
        event_data = response.event_data
        if event_data:
            print(f"  title: '{event_data.get('title', 'None')}'")
            print(f"  location: '{event_data.get('location', 'None')}'")
            print(f"  description: '{event_data.get('description', 'None')}'")
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_voice_api_endpoint())
