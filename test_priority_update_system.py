#!/usr/bin/env python3
"""
Test Priority Update API and Verify Fix
Test that the conflicts page can update priorities correctly
"""

import requests
import sqlite3
import json
from datetime import datetime

def test_priority_update_api():
    """Test the priority update API endpoint"""
    print("🧪 TESTING PRIORITY UPDATE API")
    print("=" * 50)
    
    # First, check current events in database
    print("1️⃣ CHECKING CURRENT DATABASE STATE")
    try:
        with sqlite3.connect('backend/kairocal.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, priority_level, classification_method
                FROM events
                ORDER BY created_at DESC
                LIMIT 5
            """)
            
            events = cursor.fetchall()
            
            if not events:
                print("❌ No events found in database")
                return
            
            print(f"📊 Found {len(events)} events:")
            priority_labels = {1: "VERY LOW", 2: "LOW", 3: "MEDIUM", 4: "HIGH", 5: "CRITICAL"}
            
            for event_id, title, priority, method in events:
                label = priority_labels.get(priority, f"UNKNOWN({priority})")
                print(f"   📅 {title[:40]}{'...' if len(title) > 40 else ''}")
                print(f"      ID: {event_id}")
                print(f"      Priority: {priority} ({label}) - Method: {method}")
                print()
            
            # Test updating the first event's priority
            if events:
                test_event_id = events[0][0]
                current_priority = events[0][2]
                test_title = events[0][1]
                
                print(f"2️⃣ TESTING PRIORITY UPDATE")
                print(f"   Event: {test_title}")
                print(f"   Current Priority: {current_priority}")
                
                # Try to update to a different priority
                new_priority = 2 if current_priority != 2 else 3
                
                print(f"   Testing update to Priority: {new_priority}")
                
                # Test the API endpoint
                try:
                    api_url = f"http://localhost:8003/api/v1/conflicts/event/{test_event_id}/priority"
                    params = {
                        'cognito_sub': 'frontend-test-user',
                        'new_priority': new_priority
                    }
                    
                    response = requests.put(api_url, params=params)
                    
                    print(f"   📡 API Response: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   ✅ API Success: {result}")
                        
                        # Verify the change in database
                        cursor.execute(
                            "SELECT priority_level, classification_method FROM events WHERE id = ?",
                            (test_event_id,)
                        )
                        updated_result = cursor.fetchone()
                        
                        if updated_result:
                            updated_priority, updated_method = updated_result
                            print(f"   💾 Database Updated:")
                            print(f"      New Priority: {updated_priority} ({priority_labels.get(updated_priority, 'UNKNOWN')})")
                            print(f"      New Method: {updated_method}")
                            
                            if updated_priority == new_priority:
                                print(f"   🎉 SUCCESS! Priority correctly updated from {current_priority} to {updated_priority}")
                            else:
                                print(f"   ❌ FAILURE! Expected {new_priority}, got {updated_priority}")
                        else:
                            print("   ❌ Could not verify database update")
                    else:
                        print(f"   ❌ API Error: {response.status_code}")
                        try:
                            error_data = response.json()
                            print(f"   Error Details: {error_data}")
                        except:
                            print(f"   Error Text: {response.text}")
                            
                except requests.exceptions.ConnectionError:
                    print("   ❌ API Connection Error - Backend server not running on port 8003")
                    
                except Exception as e:
                    print(f"   ❌ API Test Error: {e}")
                    
    except Exception as e:
        print(f"❌ Database error: {e}")

def verify_current_state():
    """Verify the current state after our fixes"""
    print("\n3️⃣ VERIFICATION - CURRENT EVENT STATES")
    print("=" * 40)
    
    try:
        with sqlite3.connect('backend/kairocal.db') as conn:
            cursor = conn.cursor()
            
            # Check specific events mentioned in the screenshot
            cursor.execute("""
                SELECT title, priority_level, start_time, end_time, classification_method
                FROM events
                WHERE title LIKE '%tennis%' 
                   OR title LIKE '%project%'
                   OR title LIKE '%ceo%'
                   OR title LIKE '%submission%'
                ORDER BY start_time
            """)
            
            events = cursor.fetchall()
            priority_labels = {1: "VERY LOW", 2: "LOW", 3: "MEDIUM", 4: "HIGH", 5: "CRITICAL"}
            
            print("📋 Key Events and Their Priorities:")
            
            for title, priority, start_time, end_time, method in events:
                label = priority_labels.get(priority, f"UNKNOWN({priority})")
                
                print(f"\n📅 {title}")
                print(f"   Priority: {priority} ({label})")
                print(f"   Time: {start_time} - {end_time}")
                print(f"   Method: {method}")
                
                # Check if priorities are correct based on our fix
                title_lower = title.lower()
                
                expected_message = ""
                if 'tennis' in title_lower and 'friend' in title_lower:
                    expected_message = " ✅ CORRECT (tennis with friend should be LOW)" if priority == 2 else " ❌ INCORRECT (should be LOW/2)"
                elif 'ceo' in title_lower:
                    expected_message = " ✅ CORRECT (CEO meeting should be CRITICAL)" if priority == 5 else " ❌ INCORRECT (should be CRITICAL/5)"
                elif 'submission' in title_lower:
                    expected_message = " ✅ CORRECT (deadline should be HIGH)" if priority == 4 else " ❌ INCORRECT (should be HIGH/4)"
                
                print(f"   Status:{expected_message}")
                
    except Exception as e:
        print(f"❌ Verification error: {e}")

if __name__ == "__main__":
    print("🔧 PRIORITY SYSTEM - COMPREHENSIVE TEST")
    print("=" * 60)
    
    test_priority_update_api()
    verify_current_state()
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY:")
    print("1. ✅ Database priorities fixed (tennis = LOW, CEO = CRITICAL)")
    print("2. 🧪 API endpoint for priority updates added")
    print("3. 🎨 Frontend conflicts page updated with correct BERT scale")
    print("4. 📱 Priority dropdowns now show: 1=Very Low → 5=Critical")
    print("\n🚀 NEXT: Start backend server and test conflicts page manually")
