#!/usr/bin/env python3
"""
Debug script to investigate voice parsing issues
Analyzes the specific problems reported in the bug report
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.nlp_service import NLPService
import asyncio
import re

async def debug_voice_parsing():
    """Debug the specific voice parsing issues"""
    nlp = NLPService()
    
    print("🐛 VOICE PARSING ISSUE INVESTIGATION")
    print("=" * 60)
    
    # Test cases from the bug report
    test_cases = [
        {
            "input": "Coffee Chat With Colleague At Liverpool Cafe",
            "expected_title": "Coffee Chat With Colleague",
            "expected_location": "Liverpool Cafe",
            "issue": "Location shows 'With Colleague' instead of 'Liverpool Cafe'"
        },
        {
            "input": "Explore New Hobby Craft Workshop Coming",
            "expected_title": "Explore New Hobby Craft Workshop",
            "expected_location": None,
            "issue": "'Coming' appears in title"
        },
        {
            "input": "Skating At Park Coming",
            "expected_title": "Skating",
            "expected_location": "Park",
            "issue": "'Coming' appears in title"
        },
        {
            "input": "Date With Emma Coming 7Pm",
            "expected_title": "Date With Emma",
            "expected_location": None,
            "issue": "'Coming' appears in title"
        },
        {
            "input": "Listen To Music In Free Time Coming",
            "expected_title": "Listen To Music In Free Time",
            "expected_location": None,
            "issue": "'Coming' appears in title"
        },
        {
            "input": "Meeting at Park Coming Wednesday",
            "expected_title": "Meeting",
            "expected_location": "Park",
            "issue": "Location shows 'Park Coming Wednesday'"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🔍 TEST CASE {i}: {case['issue']}")
        print(f"Input: '{case['input']}'")
        
        # Test title extraction
        extracted_title = nlp._extract_title(case['input'])
        print(f"Expected Title: '{case['expected_title']}'")
        print(f"Actual Title: '{extracted_title}'")
        title_correct = extracted_title == case['expected_title']
        print(f"Title Correct: {'✅' if title_correct else '❌'}")
        
        # Test location extraction
        extracted_location = nlp._extract_location(case['input'])
        print(f"Expected Location: '{case['expected_location']}'")
        print(f"Actual Location: '{extracted_location}'")
        location_correct = extracted_location == case['expected_location']
        print(f"Location Correct: {'✅' if location_correct else '❌'}")
        
        # Analyze the step-by-step processing
        print(f"\n🔬 STEP-BY-STEP ANALYSIS:")
        
        # Step 1: Show original text
        print(f"1. Original: '{case['input']}'")
        
        # Step 2: Show temporal removal patterns
        text = case['input'].lower()
        temporal_patterns = [
            r'\b(this|next|last|coming|upcoming)\s+(week|month|year|weekend|morning|afternoon|evening|night)\b',
            r'\b(this|next|last|coming|upcoming)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
        ]
        
        for pattern in temporal_patterns:
            before = text
            text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
            if before != text:
                print(f"2. After temporal removal ('{pattern[:20]}...'): '{text}'")
        
        # Step 3: Show location pattern matching
        print(f"3. Testing location patterns on: '{case['input']}'")
        location_patterns = [
            r'(?:at|in|@)\s+([a-zA-Z][a-zA-Z\s]+?)(?:\s+(?:at|on|for|tomorrow|today|tonight)\s|\s*$)',
            r'location\s+([a-zA-Z][a-zA-Z\s]+?)(?:\s+(?:at|on|for|tomorrow|today|tonight)\s|\s*$)',
            r'room\s+([a-zA-Z0-9]+)',
            r'conference room\s+([a-zA-Z0-9\s]+)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, case['input'], re.IGNORECASE)
            if match:
                print(f"   Pattern '{pattern[:30]}...' matched: '{match.group(1)}'")
        
        print("-" * 60)
    
    print(f"\n🎯 FINDINGS SUMMARY:")
    print("1. 'Coming' contamination: Check if temporal removal patterns are working")
    print("2. Location extraction: Check if 'at' patterns are too greedy")
    print("3. Day contamination: Check if day names are being included in location matches")

if __name__ == "__main__":
    asyncio.run(debug_voice_parsing())
