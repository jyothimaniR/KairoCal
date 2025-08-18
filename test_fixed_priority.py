#!/usr/bin/env python3
"""
Test Fixed Priority Assignment End-to-End
Test creating a new tennis event with the fixed logic
"""

import requests
import json
from datetime import datetime

def test_fixed_priority():
    """Test the fixed priority assignment"""
    print("🔧 TESTING FIXED PRIORITY ASSIGNMENT")
    print("=" * 50)
    
    # Test the same tennis event
    test_text = "tennis match with my friend today at 6:00 p.m. for 30 minutes"
    
    print(f"📝 Test Text: '{test_text}'")
    print("\n🎤 Creating voice event...")
    
    try:
        response = requests.post(
            "http://localhost:8003/api/v1/voice/create-event",
            json={"voice_text": test_text}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract priority information
            bert_classification = result.get('bert_classification', {})
            bert_priority = bert_classification.get('priority', 'unknown')
            final_priority = bert_classification.get('final_priority', 'unknown')
            confidence = bert_classification.get('confidence', 'unknown')
            
            print("✅ Event created successfully!")
            print(f"   🤖 BERT Priority: {bert_priority}")
            print(f"   🎯 Final Priority: {final_priority}")
            print(f"   📊 Confidence: {confidence}")
            
            event_id = result.get('event_id')
            if event_id:
                print(f"   🆔 Event ID: {event_id}")
                
                # Verify what was stored in database
                import sqlite3
                try:
                    with sqlite3.connect('backend/kairocal.db') as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT title, priority_level, priority_confidence, classification_method FROM events WHERE id = ?",
                            (event_id,)
                        )
                        db_result = cursor.fetchone()
                        
                        if db_result:
                            title, stored_priority, stored_confidence, method = db_result
                            print(f"\n💾 Database Storage:")
                            print(f"   Title: {title}")
                            print(f"   Stored Priority: {stored_priority}")
                            print(f"   Stored Confidence: {stored_confidence:.3f}")
                            print(f"   Method: {method}")
                            
                            # Check if fix worked
                            if stored_priority == 2:  # BERT's correct classification
                                print("\n🎉 SUCCESS! Priority correctly stored as 2 (LOW)")
                            elif stored_priority == 3:  # NLP's medium classification
                                print("\n⚠️ PARTIAL FIX: Priority stored as 3 (MEDIUM) - BERT not running")
                            else:
                                print(f"\n❌ ISSUE: Priority stored as {stored_priority} - still incorrect")
                        else:
                            print("\n❌ Event not found in database")
                except Exception as e:
                    print(f"\n❌ Database check error: {e}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("\n💡 Make sure the backend server is running on port 8003")

if __name__ == "__main__":
    test_fixed_priority()
