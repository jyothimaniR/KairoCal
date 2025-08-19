#!/usr/bin/env python3
"""
Test script to debug the actual voice processing pipeline
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.nlp_service import NLPService
import asyncio

async def test_voice_processing():
    """Test the exact voice input that's causing issues"""
    nlp = NLPService()
    
    # Test the problematic input from the screenshot
    test_input = "Play Football With Friends Coming At The Anfield Stadium"
    
    print("🎤 TESTING VOICE PROCESSING PIPELINE")
    print("=" * 60)
    print(f"Input: '{test_input}'")
    print()
    
    # Test our NLP service
    result = await nlp.process_voice_input(test_input)
    
    print("📊 NLP PROCESSING RESULT:")
    print(f"Title: '{result.get('title', 'None')}'")
    print(f"Location: '{result.get('location', 'None')}'")
    print(f"Description: '{result.get('description', 'None')}'")
    print(f"Priority: {result.get('priority', 'None')}")
    print()
    
    # Test individual methods
    print("🔍 INDIVIDUAL METHOD TESTS:")
    title = nlp._extract_title(test_input)
    location = nlp._extract_location(test_input)
    
    print(f"_extract_title(): '{title}'")
    print(f"_extract_location(): '{location}'")

if __name__ == "__main__":
    asyncio.run(test_voice_processing())
