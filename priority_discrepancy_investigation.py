#!/usr/bin/env python3
"""
Priority Discrepancy Investigation Script
Traces the exact flow from BERT classification to frontend display
"""

import requests
import json
from datetime import datetime, date
import sqlite3

def investigate_priority_discrepancy():
    """Investigate the priority mismatch between BERT and frontend display"""
    print("🔍 PRIORITY DISCREPANCY INVESTIGATION")
    print("=" * 60)
    
    # Step 1: Test BERT classification directly
    print("\n1️⃣ TESTING BERT CLASSIFICATION ENDPOINT")
    try:
        response = requests.post(
            "http://localhost:8003/api/v1/nlp/predict-priority",
            json={
                "text": "tennis match with my friend today at 5:00 p.m. for 30 minutes",
                "title": "tennis match with my friend",
                "description": "tennis match with my friend today at 5:00 p.m. for 30 minutes"
            }
        )
        
        if response.status_code == 200:
            bert_result = response.json()
            print(f"✅ BERT Result: {bert_result}")
            bert_priority = bert_result.get('priority', 'unknown')
            bert_confidence = bert_result.get('confidence', 'unknown')
            print(f"   📊 BERT Priority: {bert_priority}")
            print(f"   🎯 BERT Confidence: {bert_confidence}")
        else:
            print(f"❌ BERT API Error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ BERT API Connection Error: {e}")
        return
    
    # Step 2: Test voice event creation
    print("\n2️⃣ TESTING VOICE EVENT CREATION")
    try:
        response = requests.post(
            "http://localhost:8003/api/v1/voice/create-event",
            json={"voice_text": "tennis match with my friend today at 5:00 p.m. for 30 minutes"}
        )
        
        if response.status_code == 200:
            voice_result = response.json()
            print(f"✅ Voice Creation Result: {voice_result}")
            
            # Extract key priority information
            bert_classification = voice_result.get('bert_classification', {})
            voice_bert_priority = bert_classification.get('priority', 'unknown')
            voice_final_priority = bert_classification.get('final_priority', 'unknown')
            
            print(f"   📊 Voice BERT Priority: {voice_bert_priority}")
            print(f"   🎯 Voice Final Priority: {voice_final_priority}")
            
            # Get event ID for database check
            event_id = voice_result.get('event_id')
            if event_id:
                print(f"   🆔 Created Event ID: {event_id}")
                
                # Step 3: Check database storage
                print("\n3️⃣ CHECKING DATABASE STORAGE")
                check_database_priority(event_id)
            
        else:
            print(f"❌ Voice API Error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Voice API Connection Error: {e}")
        return
    
    # Step 4: Test events list API
    print("\n4️⃣ TESTING EVENTS LIST API")
    try:
        # Try different possible endpoints
        endpoints_to_test = [
            "http://localhost:8003/api/v1/events",
            "http://localhost:8003/api/v1/events/today",
            "http://localhost:8003/events/today",
            "http://localhost:8003/api/events",
        ]
        
        for endpoint in endpoints_to_test:
            try:
                print(f"   Testing: {endpoint}")
                response = requests.get(endpoint)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    events_data = response.json()
                    if events_data:
                        print(f"   ✅ Found {len(events_data)} events")
                        # Check first event's priority
                        first_event = events_data[0] if events_data else {}
                        if first_event:
                            event_priority = first_event.get('priority_level', first_event.get('priority', 'unknown'))
                            event_title = first_event.get('title', 'Unknown')
                            print(f"   📊 First Event: '{event_title}' -> Priority: {event_priority}")
                    else:
                        print(f"   ⚠️ Empty events list")
                    break
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    except Exception as e:
        print(f"❌ Events API Error: {e}")

def check_database_priority(event_id):
    """Check what priority is actually stored in the database"""
    try:
        # Check both possible database locations
        db_paths = [
            "kairocal.db",
            "backend/kairocal.db"
        ]
        
        for db_path in db_paths:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT title, priority_level, priority_confidence, classification_method FROM events WHERE id = ?",
                        (event_id,)
                    )
                    result = cursor.fetchone()
                    
                    if result:
                        title, priority_level, confidence, method = result
                        print(f"   📊 Database ({db_path}):")
                        print(f"      Title: {title}")
                        print(f"      Priority Level: {priority_level}")
                        print(f"      Confidence: {confidence}")
                        print(f"      Method: {method}")
                        return
            except Exception as e:
                print(f"   ⚠️ DB {db_path}: {e}")
                continue
        
        print("   ❌ Event not found in any database")
        
    except Exception as e:
        print(f"   ❌ Database Check Error: {e}")

def analyze_priority_mapping():
    """Analyze the expected vs actual priority mappings"""
    print("\n5️⃣ PRIORITY MAPPING ANALYSIS")
    print("=" * 40)
    
    print("🤖 BERT Scale (Expected):")
    print("   1 = VERY LOW")
    print("   2 = LOW") 
    print("   3 = MEDIUM")
    print("   4 = HIGH")
    print("   5 = CRITICAL")
    
    print("\n🎨 Frontend Display Issue:")
    print("   BERT Priority 2 (LOW) -> Displayed as 'HIGH'")
    print("   This suggests frontend is using inverted scale or wrong mapping")
    
    print("\n🔍 Possible Root Causes:")
    print("   1. Frontend priorityUtils.ts still using inverted conversion")
    print("   2. API returning wrong field name (priority vs priority_level)")
    print("   3. Database storing inverted values")
    print("   4. Frontend caching old priority scale")

if __name__ == "__main__":
    investigate_priority_discrepancy()
    analyze_priority_mapping()
    
    print("\n" + "=" * 60)
    print("🎯 INVESTIGATION COMPLETE")
    print("📋 Next steps: Check the specific API endpoint the frontend calls")
    print("🔧 Look for priority field mapping discrepancies")
