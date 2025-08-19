#!/usr/bin/env python3
"""
Enhanced debug script to understand the location parsing better
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.nlp_service import NLPService
import asyncio
import re

async def debug_specific_case():
    """Debug the specific location extraction issue"""
    
    test_text = "Coffee Chat With Colleague At Liverpool Cafe"
    print(f"🔍 DEBUGGING: '{test_text}'")
    print("=" * 60)
    
    # Test the location patterns manually
    clean_text = test_text
    
    # Remove time patterns first
    time_patterns_to_remove = [
        r'\b\d{1,2}:\d{2}\s*(?:a\.?m\.?|p\.?m\.?|am|pm)\b',
        r'\b\d{1,2}\s*(?:a\.?m\.?|p\.?m\.?|am|pm)\b',
        r'\b(for|lasting)\s+\d+\s*(minutes?|mins?|hours?|hrs?)\b',
        r'\b\d+\s*(minute|min|hour|hr)s?\b',
    ]
    
    for pattern in time_patterns_to_remove:
        clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE)
    
    print(f"After time removal: '{clean_text}'")
    
    # Test each location pattern
    location_patterns = [
        r'(?:at|in|@)\s+([a-zA-Z][a-zA-Z0-9\s]*?)(?:\s+(?:coming|today|tomorrow|tonight|monday|tuesday|wednesday|thursday|friday|saturday|sunday|next|this|last|with|and|or)\b|\s*$)',
        r'location\s+([a-zA-Z][a-zA-Z0-9\s]*?)(?:\s+(?:coming|today|tomorrow|tonight|monday|tuesday|wednesday|thursday|friday|saturday|sunday|next|this|last|with|and|or)\b|\s*$)',
        r'(?:conference\s+)?room\s+([a-zA-Z0-9]+)(?:\s|$)',
        r'building\s+([a-zA-Z][a-zA-Z0-9\s]*?)(?:\s+(?:coming|today|tomorrow|tonight|monday|tuesday|wednesday|thursday|friday|saturday|sunday|next|this|last|with|and|or)\b|\s*$)'
    ]
    
    for i, pattern in enumerate(location_patterns, 1):
        print(f"\nPattern {i}: {pattern}")
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            print(f"  Match found: '{location}'")
            
            # Test validation
            valid = (len(location) > 1 and 
                    not re.match(r'^\d+\s*(am|pm|a\.?m\.?|p\.?m\.?)$', location, re.IGNORECASE) and
                    not re.match(r'^\d+\s*(minute|min|hour|hr)', location, re.IGNORECASE) and
                    not re.search(r'\b(coming|with|colleague|emma|friends|time|free|and|or)\b', location, re.IGNORECASE) and
                    not re.match(r'^[A-Z][a-z]+\s+(and\s+)?[A-Z][a-z]+$', location))
            
            print(f"  Valid: {valid}")
            if not valid:
                print(f"  Rejected because: contains forbidden words or is person name")
            else:
                location = re.sub(r'\s+(coming|with|and|or).*$', '', location, flags=re.IGNORECASE).strip()
                print(f"  Final location: '{location}'")
        else:
            print(f"  No match")

if __name__ == "__main__":
    asyncio.run(debug_specific_case())
