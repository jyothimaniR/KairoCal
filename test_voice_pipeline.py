#!/usr/bin/env python3
"""
Test script to debug the full voice processing pipeline
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.nlp_service import NLPService
from backend.app.nlp.temporal_resolver import TemporalResolver

async def test_voice_processing():
    print('=== Testing Full Voice Processing Pipeline ===')
    print(f'Current time: {datetime.now()}')
    print()
    
    nlp_service = NLPService()
    
    test_cases = [
        'schedule meeting with CEO tomorrow at 2 pm',
        'call mom at 6pm today',
        'lunch meeting tomorrow 2pm',
        'doctor appointment at 2:00 pm tomorrow',
        'meeting at 2 PM',
        'coffee at 3:30pm'
    ]
    
    for voice_text in test_cases:
        print(f'Testing: "{voice_text}"')
        try:
            result = await nlp_service.process_voice_input(voice_text)
            
            print(f'  Title: {result.get("title")}')
            print(f'  Start time: {result.get("start_time")}')
            print(f'  End time: {result.get("end_time")}')
            print(f'  Priority: {result.get("priority")}')
            print(f'  Event type: {result.get("event_type")}')
            
            # Show the actual datetime objects
            start_time = result.get("start_time")
            if start_time:
                if isinstance(start_time, str):
                    print(f'  Start time type: string - {start_time}')
                else:
                    print(f'  Start time formatted: {start_time.strftime("%Y-%m-%d %H:%M:%S")} (Hour: {start_time.hour})')
            
        except Exception as e:
            print(f'  ERROR: {e}')
        print()

if __name__ == '__main__':
    asyncio.run(test_voice_processing())
