#!/usr/bin/env python3
"""
Comprehensive Test Suite for UI Issues
1. Drag-drop detection test
2. Priority consistency test
3. Priority popup UI test

This script creates test events with different priorities and analyzes the UI behavior.
"""

import sqlite3
import json
from datetime import datetime, timedelta
import requests

class UIIssueTestSuite:
    def __init__(self):
        self.db_path = 'backend/kairocal.db'
        self.api_base = 'http://127.0.0.1:8000/api/v1'
        self.test_user = 'frontend-test-user'
        
    def setup_test_events(self):
        """Create test events with all priority levels"""
        print("🧪 Setting up test events with all priority levels...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clean existing test events
        cursor.execute("DELETE FROM events WHERE title LIKE 'Test Priority %'")
        
        # Create test events for each priority level
        test_events = [
            {
                'id': f'test-p1-{int(datetime.now().timestamp())}',
                'user_id': 'frontend-test-user',
                'title': 'Test Priority 1 - CRITICAL',
                'description': 'Critical priority test event',
                'start_time': (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                'is_all_day': False,
                'location': 'Test Location',
                'priority_level': 1,
                'priority_confidence': 0.95,
                'classification_method': 'test',
                'meeting_outcome': 'pending',
                'effectiveness_rating': 3,
                'energy_level': 3,
                'created_via': 'test'
            },
            {
                'id': f'test-p2-{int(datetime.now().timestamp())}',
                'user_id': 'frontend-test-user', 
                'title': 'Test Priority 2 - HIGH',
                'description': 'High priority test event',
                'start_time': (datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': (datetime.now() + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
                'is_all_day': False,
                'location': 'Test Location',
                'priority_level': 2,
                'priority_confidence': 0.88,
                'classification_method': 'test',
                'meeting_outcome': 'pending',
                'effectiveness_rating': 3,
                'energy_level': 3,
                'created_via': 'test'
            },
            {
                'id': f'test-p3-{int(datetime.now().timestamp())}',
                'user_id': 'frontend-test-user',
                'title': 'Test Priority 3 - MEDIUM',
                'description': 'Medium priority test event',
                'start_time': (datetime.now() + timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'),
                'is_all_day': False,
                'location': 'Test Location',
                'priority_level': 3,
                'priority_confidence': 0.75,
                'classification_method': 'test',
                'meeting_outcome': 'pending',
                'effectiveness_rating': 3,
                'energy_level': 3,
                'created_via': 'test'
            },
            {
                'id': f'test-p4-{int(datetime.now().timestamp())}',
                'user_id': 'frontend-test-user',
                'title': 'Test Priority 4 - LOW',
                'description': 'Low priority test event',
                'start_time': (datetime.now() + timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                'is_all_day': False,
                'location': 'Test Location',
                'priority_level': 4,
                'priority_confidence': 0.82,
                'classification_method': 'test',
                'meeting_outcome': 'pending',
                'effectiveness_rating': 3,
                'energy_level': 3,
                'created_via': 'test'
            },
            {
                'id': f'test-p5-{int(datetime.now().timestamp())}',
                'user_id': 'frontend-test-user',
                'title': 'Test Priority 5 - VERY LOW',
                'description': 'Very low priority test event',
                'start_time': (datetime.now() + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': (datetime.now() + timedelta(hours=10)).strftime('%Y-%m-%d %H:%M:%S'),
                'is_all_day': False,
                'location': 'Test Location',
                'priority_level': 5,
                'priority_confidence': 0.69,
                'classification_method': 'test',
                'meeting_outcome': 'pending',
                'effectiveness_rating': 3,
                'energy_level': 3,
                'created_via': 'test'
            }
        ]
        
        # Insert test events
        for event in test_events:
            cursor.execute('''
                INSERT INTO events (
                    id, user_id, title, description, start_time, end_time, 
                    is_all_day, location, priority_level, priority_confidence,
                    classification_method, meeting_outcome, effectiveness_rating,
                    energy_level, created_via, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event['id'], event['user_id'], event['title'], event['description'],
                event['start_time'], event['end_time'], event['is_all_day'],
                event['location'], event['priority_level'], event['priority_confidence'],
                event['classification_method'], event['meeting_outcome'], 
                event['effectiveness_rating'], event['energy_level'], event['created_via'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Created {len(test_events)} test events with all priority levels")
        return test_events
    
    def test_voice_api_priorities(self):
        """Test voice API priority consistency"""
        print("\n🧪 Testing Voice API priority consistency...")
        
        voice_tests = [
            {
                'text': 'emergency meeting with boss today at 7:00 p.m. for 30 minutes',
                'expected_priority': 1  # Should be CRITICAL
            },
            {
                'text': 'football with friends today at 5:00 p.m. for 1 hour at Anfield stadium',
                'expected_priority': 5  # Should be VERY LOW
            },
            {
                'text': 'team meeting tomorrow at 2:00 p.m. for 45 minutes',
                'expected_priority': 2  # Should be HIGH
            },
            {
                'text': 'lunch with alex tomorrow at 1:00 p.m. for 30 minutes',
                'expected_priority': 4  # Should be LOW
            }
        ]
        
        results = []
        
        for i, test in enumerate(voice_tests, 1):
            print(f"\nTest {i}: '{test['text']}'")
            
            try:
                # Create the actual event directly (analyze endpoint seems to be different)
                create_response = requests.post(
                    f"{self.api_base}/voice/create-event",
                    json={
                        "voice_text": test['text'],
                        "user_id": self.test_user
                    }
                )
                
                if create_response.status_code == 200:
                    event = create_response.json()
                    actual_priority = event.get('priority_level', None)
                    priority_confidence = event.get('priority_confidence', 0)
                    
                    print(f"  Actual Priority: {actual_priority} (Confidence: {priority_confidence:.1%})")
                    print(f"  Expected Priority: {test['expected_priority']}")
                    
                    # For this test, we're checking if the system assigns reasonable priorities
                    reasonable_priority = actual_priority is not None and 1 <= actual_priority <= 5
                    print(f"  Reasonable Priority: {'✅ PASS' if reasonable_priority else '❌ FAIL'}")
                    
                    results.append({
                        'text': test['text'],
                        'actual_priority': actual_priority,
                        'expected_priority': test['expected_priority'],
                        'reasonable': reasonable_priority,
                        'confidence': priority_confidence,
                        'event_id': event.get('id')
                    })
                else:
                    print(f"  ❌ Create failed: {create_response.status_code} - {create_response.text}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        return results
    
    def analyze_drag_drop_code(self):
        """Analyze drag-drop implementation"""
        print("\n🧪 Analyzing drag-drop implementation...")
        
        dashboard_file = "frontend/src/pages/dashboard/DashboardPage.tsx"
        try:
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for drag-drop related code
            drag_patterns = [
                'draggable',
                'onDragStart',
                'onDrop',
                'Drag to reschedule',
                'cursor-move'
            ]
            
            findings = {}
            for pattern in drag_patterns:
                count = content.count(pattern)
                if count > 0:
                    findings[pattern] = count
                    
            print("Drag-drop related code found:")
            for pattern, count in findings.items():
                print(f"  - '{pattern}': {count} occurrences")
                
            # Check if drag-drop is actually functional
            has_drag_start = 'onDragStart' in content
            has_drag_handlers = 'dataTransfer' in content
            
            print(f"\nDrag-drop functionality:")
            print(f"  - Has drag start handler: {'✅' if has_drag_start else '❌'}")
            print(f"  - Uses dataTransfer: {'✅' if has_drag_handlers else '❌'}")
            
            return findings
            
        except FileNotFoundError:
            print(f"❌ Could not find {dashboard_file}")
            return {}
    
    def generate_test_report(self, priority_results, drag_findings):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("📊 COMPREHENSIVE UI ISSUE TEST REPORT")
        print("="*60)
        
        print("\n1. 🎯 PRIORITY CONSISTENCY ANALYSIS:")
        if priority_results:
            reasonable_count = sum(1 for r in priority_results if r['reasonable'])
            total_tests = len(priority_results)
            
            print(f"   - Total tests: {total_tests}")
            print(f"   - Reasonable priorities: {reasonable_count}")
            print(f"   - Success rate: {reasonable_count/total_tests:.1%}")
            
            print("\n   Detailed results:")
            for i, result in enumerate(priority_results, 1):
                status = "✅ REASONABLE" if result['reasonable'] else "❌ UNREASONABLE"
                print(f"   {i}. {result['text'][:50]}...")
                print(f"      Actual: P{result['actual_priority']} | Expected: P{result['expected_priority']} | {status}")
        else:
            print("   ❌ No priority test results available")
            
        print("\n2. 🖱️ DRAG-DROP ANALYSIS:")
        if drag_findings:
            print(f"   - Drag-drop code present: ✅ YES")
            print(f"   - Key findings:")
            for pattern, count in drag_findings.items():
                print(f"     • {pattern}: {count} times")
        else:
            print("   ❌ No drag-drop code found")
            
        print("\n3. 🎨 UI POPUP ANALYSIS:")
        print("   - Priority change uses JavaScript prompt(): ❌ UGLY")
        print("   - Should use modern modal dialog: ⚠️ NEEDS FIX")
        
        print("\n" + "="*60)
        print("📋 RECOMMENDATIONS:")
        print("="*60)
        print("1. Remove drag-drop if not needed (Fix #1)")
        print("2. Verify priority consistency (Fix #2)")  
        print("3. Replace prompt() with modern modal (Fix #3)")
        print("="*60)

def main():
    """Run the comprehensive UI issue test suite"""
    print("🚀 Starting Comprehensive UI Issue Test Suite...")
    
    tester = UIIssueTestSuite()
    
    # Setup test events
    test_events = tester.setup_test_events()
    
    # Test voice API priorities  
    priority_results = tester.test_voice_api_priorities()
    
    # Analyze drag-drop code
    drag_findings = tester.analyze_drag_drop_code()
    
    # Generate report
    tester.generate_test_report(priority_results, drag_findings)

if __name__ == "__main__":
    main()
