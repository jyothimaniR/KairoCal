#!/usr/bin/env python3
"""
Debug Voice Priority Assignment
Test the exact same text that caused the discrepancy
"""

import sys
import os
sys.path.append('backend')

from app.services.nlp_service import NLPService
import asyncio

async def debug_voice_priority():
    """Debug the exact priority assignment for tennis event"""
    print("🔍 DEBUGGING VOICE PRIORITY ASSIGNMENT")
    print("=" * 50)
    
    # The exact text from the screenshot
    test_text = "tennis match with my friend today at 5:00 p.m. for 30 minutes"
    
    print(f"📝 Test Text: '{test_text}'")
    print()
    
    # Initialize NLP service
    nlp_service = NLPService()
    
    # Step 1: Test enhanced priority detection directly
    print("1️⃣ TESTING ENHANCED NLP PRIORITY DETECTION")
    nlp_priority = nlp_service._enhanced_priority_detection(test_text)
    print(f"   🎯 Enhanced NLP Priority: {nlp_priority}")
    
    # Step 2: Test full voice processing
    print("\n2️⃣ TESTING FULL VOICE PROCESSING")
    voice_result = await nlp_service.process_voice_input(test_text)
    voice_priority = voice_result.get('priority', 'unknown')
    print(f"   📊 Voice Processing Priority: {voice_priority}")
    print(f"   📋 Full Voice Result: {voice_result}")
    
    # Step 3: Test BERT classification
    print("\n3️⃣ TESTING BERT CLASSIFICATION")
    try:
        from app.nlp.model_loader import get_global_bert_model
        bert_model = get_global_bert_model()
        
        if bert_model and bert_model.is_trained:
            # Prepare event data for BERT (same as voice.py)
            event_for_bert = {
                'title': voice_result.get('title', 'Voice Event'),
                'description': voice_result.get('description', test_text),
                'start_time': voice_result.get('start_time', ''),
                'location': voice_result.get('location', '')
            }
            
            bert_priority, bert_confidence = bert_model.predict(event_for_bert)
            print(f"   🤖 BERT Priority: {bert_priority}")
            print(f"   🎯 BERT Confidence: {bert_confidence:.3f}")
            
            # Step 4: Simulate the hybrid decision logic
            print("\n4️⃣ SIMULATING HYBRID DECISION LOGIC")
            print(f"   📊 NLP Priority: {nlp_priority}")
            print(f"   🤖 BERT Priority: {bert_priority} (confidence: {bert_confidence:.3f})")
            
            # Reproduce the exact logic from voice.py
            if nlp_priority >= 4 and nlp_priority > bert_priority:
                final_priority = nlp_priority
                print(f"   🎯 HYBRID RESULT: Using NLP priority {nlp_priority} (keyword-based critical event)")
            elif bert_confidence >= 0.7 and bert_priority >= nlp_priority:
                final_priority = bert_priority
                print(f"   🎯 HYBRID RESULT: Using BERT priority {bert_priority} (high confidence)")
            else:
                final_priority = round((nlp_priority * 0.6) + (bert_priority * 0.4))
                final_priority = max(1, min(5, final_priority))
                print(f"   🎯 HYBRID RESULT: Using weighted priority {final_priority} (NLP: {nlp_priority}, BERT: {bert_priority})")
            
            print(f"\n🚨 FINAL PRIORITY THAT GETS STORED: {final_priority}")
            
        else:
            print("   ❌ BERT model not available")
            
    except Exception as e:
        print(f"   ❌ BERT test error: {e}")

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(debug_voice_priority())
    
    print("\n" + "=" * 50)
    print("🔍 ROOT CAUSE ANALYSIS:")
    print("- BERT correctly classifies tennis as LOW (priority 2)")
    print("- But NLP enhanced detection might be assigning higher priority")
    print("- Hybrid logic then overrides BERT with the wrong value")
    print("- Solution: Fix the hybrid logic or NLP priority keywords")

if __name__ == "__main__":
    main()
