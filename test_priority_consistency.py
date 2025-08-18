#!/usr/bin/env python3
"""
Priority Consistency Test Script

Tests the voice API to ensure priorities are correctly assigned and displayed.
This tests Fix #2 - ensuring preview priorities match actual event priorities.
"""

import requests
import sqlite3
from datetime import datetime
import json

class PriorityConsistencyTester:
    def __init__(self):
        self.api_base = 'http://127.0.0.1:8000/api/v1'
        self.db_path = 'backend/kairocal.db'
        self.test_user = 'frontend-test-user'
    
    def test_voice_priority_assignments(self):
        """Test voice API priority assignments with various event types"""
        print("🧪 Testing Voice API Priority Assignments...")
        
        test_cases = [
            {
                'input': 'emergency meeting with CEO right now for 30 minutes',
                'expected_range': [1, 2],  # Should be CRITICAL or HIGH
                'description': 'Emergency CEO meeting'
            },
            {
                'input': 'doctor appointment tomorrow at 2 pm for 1 hour',
                'expected_range': [2, 3],  # Should be HIGH or MEDIUM
                'description': 'Medical appointment'
            },
            {
                'input': 'team standup meeting tomorrow at 9 am for 15 minutes',
                'expected_range': [2, 3],  # Should be HIGH or MEDIUM
                'description': 'Regular team meeting'
            },
            {
                'input': 'lunch with sarah tomorrow at noon for 1 hour',
                'expected_range': [3, 4],  # Should be MEDIUM or LOW
                'description': 'Casual lunch meeting'
            },
            {
                'input': 'coffee break today at 3 pm for 15 minutes',
                'expected_range': [4, 5],  # Should be LOW or VERY LOW
                'description': 'Coffee break'
            },
            {
                'input': 'football game with friends this weekend for 2 hours',
                'expected_range': [4, 5],  # Should be LOW or VERY LOW
                'description': 'Social activity'
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test_case['description']}")
            print(f"Input: '{test_case['input']}'")
            
            try:
                # Create event via voice API
                response = requests.post(
                    f"{self.api_base}/voice/create-event",
                    json={
                        "voice_text": test_case['input'],
                        "user_id": self.test_user
                    }
                )
                
                if response.status_code == 200:
                    event_response = response.json()
                    event = event_response.get('event_data', {})
                    bert_info = event_response.get('bert_classification', {})
                    
                    actual_priority = event.get('priority_level') or bert_info.get('priority')
                    confidence = event.get('priority_confidence') or bert_info.get('confidence', 0)
                    event_id = event.get('id') or event_response.get('event_id')
                    
                    # Check if priority is in expected range
                    in_range = (actual_priority >= test_case['expected_range'][0] and 
                              actual_priority <= test_case['expected_range'][1])
                    
                    print(f"  Assigned Priority: {actual_priority}")
                    print(f"  Expected Range: {test_case['expected_range'][0]}-{test_case['expected_range'][1]}")
                    print(f"  Confidence: {confidence:.1%}")
                    print(f"  In Expected Range: {'✅ YES' if in_range else '❌ NO'}")
                    
                    results.append({
                        'test_case': test_case['description'],
                        'input': test_case['input'],
                        'expected_range': test_case['expected_range'],
                        'actual_priority': actual_priority,
                        'confidence': confidence,
                        'in_range': in_range,
                        'event_id': event_id
                    })
                    
                else:
                    print(f"  ❌ API Error: {response.status_code}")
                    print(f"  Response: {response.text}")
                    
            except Exception as e:
                print(f"  ❌ Exception: {e}")
        
        return results
    
    def verify_database_consistency(self, results):
        """Verify that database values match API responses"""
        print("\n🔍 Verifying Database Consistency...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        consistent_count = 0
        total_count = len([r for r in results if r.get('event_id')])
        
        for result in results:
            event_id = result.get('event_id')
            if not event_id:
                continue
                
            cursor.execute(
                "SELECT priority_level, priority_confidence FROM events WHERE id = ?",
                (event_id,)
            )
            
            db_result = cursor.fetchone()
            if db_result:
                db_priority, db_confidence = db_result
                api_priority = result['actual_priority']
                api_confidence = result['confidence']
                
                priority_match = db_priority == api_priority
                confidence_match = abs(db_confidence - api_confidence) < 0.01  # Allow small float differences
                
                if priority_match and confidence_match:
                    consistent_count += 1
                    print(f"  ✅ {result['test_case']}: DB matches API")
                else:
                    print(f"  ❌ {result['test_case']}: MISMATCH")
                    print(f"    API: P{api_priority} ({api_confidence:.1%})")
                    print(f"    DB:  P{db_priority} ({db_confidence:.1%})")
        
        conn.close()
        
        consistency_rate = consistent_count / total_count if total_count > 0 else 0
        print(f"\n📊 Database Consistency: {consistent_count}/{total_count} ({consistency_rate:.1%})")
        
        return consistency_rate >= 0.95  # 95% consistency threshold
    
    def generate_priority_test_report(self, results, db_consistent):
        """Generate comprehensive priority test report"""
        print("\n" + "="*60)
        print("📊 PRIORITY CONSISTENCY TEST REPORT")
        print("="*60)
        
        if not results:
            print("❌ No test results available")
            return
            
        # Calculate statistics
        total_tests = len(results)
        in_range_count = sum(1 for r in results if r['in_range'])
        high_confidence_count = sum(1 for r in results if r['confidence'] >= 0.8)
        
        print(f"\n🎯 PRIORITY ASSIGNMENT ANALYSIS:")
        print(f"   - Total tests: {total_tests}")
        print(f"   - In expected range: {in_range_count}/{total_tests} ({in_range_count/total_tests:.1%})")
        print(f"   - High confidence (≥80%): {high_confidence_count}/{total_tests} ({high_confidence_count/total_tests:.1%})")
        print(f"   - Database consistency: {'✅ PASS' if db_consistent else '❌ FAIL'}")
        
        print(f"\n📋 DETAILED RESULTS:")
        for i, result in enumerate(results, 1):
            status = "✅ PASS" if result['in_range'] else "❌ FAIL"
            print(f"   {i}. {result['test_case']}")
            print(f"      Input: {result['input'][:50]}...")
            print(f"      Expected: P{result['expected_range'][0]}-{result['expected_range'][1]} | Actual: P{result['actual_priority']} | {status}")
            print(f"      Confidence: {result['confidence']:.1%}")
        
        # Overall assessment
        overall_pass = (in_range_count / total_tests) >= 0.7 and db_consistent
        print(f"\n🏆 OVERALL ASSESSMENT: {'✅ SYSTEM WORKING CORRECTLY' if overall_pass else '❌ NEEDS IMPROVEMENT'}")
        
        if not overall_pass:
            print("\n⚠️  ISSUES IDENTIFIED:")
            if (in_range_count / total_tests) < 0.7:
                print("   - Priority assignments not matching expected ranges")
            if not db_consistent:
                print("   - Database values don't match API responses")
        
        print("="*60)

def main():
    """Run the priority consistency test suite"""
    print("🚀 Starting Priority Consistency Test Suite...")
    
    tester = PriorityConsistencyTester()
    
    # Test voice API priority assignments
    results = tester.test_voice_priority_assignments()
    
    # Verify database consistency
    db_consistent = tester.verify_database_consistency(results)
    
    # Generate comprehensive report
    tester.generate_priority_test_report(results, db_consistent)

if __name__ == "__main__":
    main()
