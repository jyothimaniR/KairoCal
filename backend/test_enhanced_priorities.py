#!/usr/bin/env python3
"""
Quick test for enhanced priority keywords
Tests the CEO and surgery priority issues specifically
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.nlp_service import NLPService
import asyncio

async def test_enhanced_priorities():
    """Test the enhanced priority keyword system"""
    nlp = NLPService()
    
    # Test cases from your voice samples
    test_cases = [
        {
            "text": "schedule a meeting with the CEO tomorrow at 12",
            "expected_priority": 5,
            "description": "Meeting with CEO"
        },
        {
            "text": "schedule a meeting with Dr Paul for heart surgery at 11:00 a.m. in the morning at Liverpool Hospital",
            "expected_priority": 5,
            "description": "Heart surgery appointment"
        },
        {
            "text": "up a meeting with detecting for implementing the new feature for our website at 10:00 a.m. tomorrow at boardroom",
            "expected_priority": 3,
            "description": "Regular development meeting"
        },
        {
            "text": "learn a Hangout with friends",
            "expected_priority": 1,
            "description": "Casual hangout"
        },
        {
            "text": "urgent meeting with board of directors",
            "expected_priority": 5,
            "description": "Urgent board meeting"
        },
        {
            "text": "coffee with colleagues",
            "expected_priority": 2,
            "description": "Casual coffee"
        },
        {
            "text": "emergency doctor appointment for surgery consultation",
            "expected_priority": 5,
            "description": "Emergency medical"
        }
    ]
    
    print("🧪 Testing Enhanced Priority Keywords")
    print("=" * 60)
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['description']}")
        print(f"🗣️ Text: '{test['text']}'")
        
        try:
            # Process the text
            result = await nlp.process_voice_input(test['text'])
            predicted_priority = result.get('priority', 3)
            expected_priority = test['expected_priority']
            
            # Check if prediction is correct or close
            is_correct = predicted_priority == expected_priority
            is_close = abs(predicted_priority - expected_priority) <= 1
            
            if is_correct:
                status = "✅ CORRECT"
                correct_predictions += 1
            elif is_close:
                status = "⚠️ CLOSE"
            else:
                status = "❌ WRONG"
            
            priority_labels = {
                5: "🔴 CRITICAL/URGENT",
                4: "🟠 IMPORTANT/HIGH", 
                3: "🟡 NORMAL/MEDIUM",
                2: "🔵 LOW PRIORITY",
                1: "⚪ VERY LOW"
            }
            
            print(f"🎯 Expected: Priority {expected_priority} ({priority_labels.get(expected_priority, 'Unknown')})")
            print(f"🤖 Predicted: Priority {predicted_priority} ({priority_labels.get(predicted_priority, 'Unknown')})")
            print(f"📊 Status: {status}")
            
        except Exception as e:
            print(f"❌ Error processing test: {e}")
    
    # Summary
    accuracy = (correct_predictions / total_tests) * 100
    print(f"\n" + "=" * 60)
    print(f"📊 RESULTS SUMMARY")
    print(f"=" * 60)
    print(f"✅ Correct Predictions: {correct_predictions}/{total_tests}")
    print(f"🎯 Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 70:
        print(f"🎉 EXCELLENT! Enhanced keywords working well!")
        if correct_predictions >= total_tests - 1:
            print(f"🏆 PERFECT! CEO and surgery priorities should now be CRITICAL!")
    else:
        print(f"⚠️ Needs improvement. Target accuracy: 70%+")
    
    return accuracy >= 70

if __name__ == "__main__":
    success = asyncio.run(test_enhanced_priorities())
    print(f"\n🏁 Test {'PASSED' if success else 'FAILED'}")
