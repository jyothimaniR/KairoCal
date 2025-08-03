#!/usr/bin/env python3
"""
Test Enhanced Priority Detection Directly
Verifies that our enhanced system works before API integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.nlp_service import NLPService
import asyncio

async def test_priority_detection_direct():
    """Test priority detection directly from NLP service"""
    nlp = NLPService()
    
    print("🧪 Testing Enhanced Priority Detection (Direct)")
    print("=" * 60)
    
    test_cases = [
        "meeting with the CEO tomorrow at 12",
        "schedule a meeting with Dr Paul for heart surgery",
        "hangout with friends at Starbucks",
        "urgent board meeting",
        "coffee with colleagues"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: '{text}'")
        
        # Test the enhanced priority detection directly
        priority = nlp._enhanced_priority_detection(text)
        
        # Also test through full NLP processing
        result = await nlp.process_voice_input(text)
        nlp_priority = result.get('priority', 3)
        
        print(f"🔍 Enhanced Detection: Priority {priority}")
        print(f"📊 Full NLP Processing: Priority {nlp_priority}")
        
        # Check for critical keywords
        if any(keyword in text.lower() for keyword in ['ceo', 'surgery', 'heart surgery']):
            if priority >= 5:
                print("✅ CORRECT: Critical event detected as Priority 5")
            else:
                print(f"❌ ISSUE: Critical event only got Priority {priority}")
        
        if 'friends' in text.lower() or 'hangout' in text.lower():
            if priority <= 2:
                print("✅ CORRECT: Social event detected as low priority")
            else:
                print(f"⚠️ ISSUE: Social event got Priority {priority}")

if __name__ == "__main__":
    asyncio.run(test_priority_detection_direct())
