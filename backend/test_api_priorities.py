#!/usr/bin/env python3
"""
Test Enhanced Priority System with Actual Voice API
"""

import requests
import json

def test_enhanced_api_priorities():
    """Test the enhanced priority system through the actual API"""
    api_url = "http://localhost:8001/api/v1/voice/analyze-voice"
    
    test_cases = [
        {
            "text": "schedule a meeting with the CEO tomorrow at 12",
            "expected_priority": 5,
            "description": "CEO Meeting (should be CRITICAL)"
        },
        {
            "text": "schedule a meeting with Dr Paul for heart surgery at 11:00 a.m.",
            "expected_priority": 5,
            "description": "Heart Surgery (should be CRITICAL)"
        },
        {
            "text": "hangout with friends at Starbucks",
            "expected_priority": 1,
            "description": "Casual Hangout (should be VERY LOW)"
        }
    ]
    
    print("🧪 Testing Enhanced Priority System via API")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['description']}")
        print(f"🗣️ Text: '{test['text']}'")
        
        try:
            params = {
                "voice_text": test['text'],
                "user_id": 1
            }
            
            response = requests.post(api_url, params=params, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract priority from different possible locations
                priority = None
                if "bert_analysis" in result:
                    priority = result["bert_analysis"].get("priority")
                elif "recommended_event" in result:
                    priority = result["recommended_event"].get("priority")
                elif "nlp_analysis" in result:
                    priority = result["nlp_analysis"].get("priority")
                
                expected = test['expected_priority']
                
                if priority == expected:
                    status = "✅ CORRECT"
                elif priority and abs(priority - expected) <= 1:
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
                
                print(f"🎯 Expected: Priority {expected} ({priority_labels.get(expected, 'Unknown')})")
                print(f"🤖 API Result: Priority {priority} ({priority_labels.get(priority, 'Unknown')})")
                print(f"📊 Status: {status}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_enhanced_api_priorities()
