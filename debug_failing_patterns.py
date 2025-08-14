#!/usr/bin/env python3
"""
Debug the specific failing voice patterns to find the root cause
"""

import asyncio
import sys
import os
import re
from datetime import datetime

# Add the backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.nlp_service import NLPService
from backend.app.nlp.temporal_resolver import TemporalResolver

async def debug_failing_patterns():
    print('=== Debugging Failing Voice Patterns ===')
    print(f'Current time: {datetime.now()}')
    print()
    
    nlp_service = NLPService()
    resolver = TemporalResolver()
    
    failing_cases = [
        "set up a lunch tomorrow with my friend at 2:00 p.m.",
        "schedule me a lunch with my friends today at 2:30 p.m.",
    ]
    
    working_cases = [
        "Schedule lunch tomorrow at 2 PM",
        "Lunch at 12:30pm tomorrow"
    ]
    
    all_cases = [
        ("FAILING", failing_cases),
        ("WORKING", working_cases)
    ]
    
    for case_type, cases in all_cases:
        print(f'=== {case_type} CASES ===')
        
        for voice_text in cases:
            print(f'Voice text: "{voice_text}"')
            
            # Step 1: Check voice cleaning
            processor = nlp_service.VoiceProcessor() if hasattr(nlp_service, 'VoiceProcessor') else None
            if hasattr(nlp_service, '_clean_voice_text'):
                cleaned = nlp_service._clean_voice_text(voice_text)
                print(f'  Cleaned: "{cleaned}"')
            else:
                cleaned = voice_text.lower()
                print(f'  Cleaned (simple): "{cleaned}"')
            
            # Step 2: Test time extraction functions in voice API
            def _extract_time_token(text: str):
                import re
                patterns = [
                    r"\b\d{1,2}:\d{2}\s*(?:a\.?m\.?|p\.?m\.?|am|pm)\b",
                    r"\b\d{1,2}\s*(?:a\.?m\.?|p\.?m\.?|am|pm)\b",
                    r"\b\d{1,2}:\d{2}\b",
                    r"\b(noon|midnight|morning|afternoon|evening|night)\b"
                ]
                for p in patterns:
                    m = re.search(p, text, flags=re.IGNORECASE)
                    if m:
                        return m.group(0)
                return None
            
            def _has_explicit_time(text: str) -> bool:
                import re
                explicit = re.search(r"\b(\d{1,2}(:\d{2})?\s*(am|pm)|noon|midnight)\b", text, re.IGNORECASE)
                return bool(explicit)
            
            time_token = _extract_time_token(cleaned)
            has_time = _has_explicit_time(cleaned)
            
            print(f'  Time token: "{time_token}"')
            print(f'  Has explicit time: {has_time}')
            
            # Step 3: Test temporal resolver directly
            if time_token:
                try:
                    start_dt, end_dt = resolver.resolve_full_temporal('tomorrow', time_token, None, 'lunch')
                    print(f'  Temporal resolver result: {start_dt} -> {end_dt}')
                    if start_dt:
                        print(f'  Hour: {start_dt.hour}, Minute: {start_dt.minute}')
                except Exception as e:
                    print(f'  Temporal resolver error: {e}')
            
            # Step 4: Test NLP service processing
            try:
                result = await nlp_service.process_voice_input(voice_text)
                print(f'  NLP result - Title: {result.get("title")}')
                print(f'  NLP result - Start: {result.get("start_time")}')
                print(f'  NLP result - Location: {result.get("location")}')
                
                start_time = result.get("start_time")
                if start_time and hasattr(start_time, 'hour'):
                    print(f'  NLP result - Hour: {start_time.hour}, Minute: {start_time.minute}')
                
            except Exception as e:
                print(f'  NLP processing error: {e}')
            
            print()

if __name__ == '__main__':
    asyncio.run(debug_failing_patterns())
