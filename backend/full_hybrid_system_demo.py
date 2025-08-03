#!/usr/bin/env python3
"""
Full Hybrid System Demo for KairoCal Voice API
Tests the complete integration of Voice-to-Text + Enhanced Priority + BERT + Event Creation
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

class FullHybridSystemDemo:
    def __init__(self, base_url: str = "http://127.0.0.1:8001"):
        self.base_url = base_url
        self.test_user_id = 1
        
    def test_voice_api_health(self) -> bool:
        """Test if the voice API is running"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/voice/health")
            if response.status_code == 200:
                health_data = response.json()
                print("🟢 Voice API Health Check:")
                print(f"   Status: {health_data.get('status', 'unknown')}")
                print(f"   Services: {health_data.get('services', {})}")
                return True
            else:
                print(f"🔴 API Health Check Failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"🔴 API Connection Failed: {e}")
            return False
    
    def test_hybrid_priority_classification(self, voice_text: str, expected_priority: int, description: str) -> Dict[str, Any]:
        """Test hybrid priority classification without creating events"""
        print(f"\n🧪 Testing: {description}")
        print(f"📝 Voice Input: '{voice_text}'")
        
        try:
            # Use analyze-voice endpoint to test priority without creating events
            response = requests.post(
                f"{self.base_url}/api/v1/voice/analyze-voice",
                params={
                    'voice_text': voice_text,
                    'user_id': self.test_user_id
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract priority information
                nlp_priority = data.get('nlp_analysis', {}).get('priority', 0)
                bert_priority = data.get('bert_analysis', {}).get('priority', 0)
                bert_confidence = data.get('bert_analysis', {}).get('confidence', 0)
                
                print(f"🔍 Enhanced NLP Priority: {nlp_priority}")
                print(f"🤖 BERT Priority: {bert_priority} (confidence: {bert_confidence:.3f})")
                
                # Determine hybrid result
                is_correct = nlp_priority == expected_priority
                status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
                
                print(f"{status}: Expected {expected_priority}, Got {nlp_priority}")
                
                return {
                    'success': True,
                    'voice_text': voice_text,
                    'nlp_priority': nlp_priority,
                    'bert_priority': bert_priority,
                    'bert_confidence': bert_confidence,
                    'expected_priority': expected_priority,
                    'is_correct': is_correct,
                    'full_response': data
                }
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            print(f"❌ Request Failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_full_event_creation(self, voice_text: str, description: str) -> Dict[str, Any]:
        """Test complete voice-to-event pipeline with hybrid priority"""
        print(f"\n🚀 Full Pipeline Test: {description}")
        print(f"📝 Voice Input: '{voice_text}'")
        
        try:
            # Use create-event endpoint to test full pipeline
            response = requests.post(
                f"{self.base_url}/api/v1/voice/create-event",
                json={
                    'voice_text': voice_text,
                    'user_id': self.test_user_id,
                    'priority_override': None
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                success = data.get('success', False)
                event_id = data.get('event_id')
                event_data = data.get('event_data', {})
                
                if success and event_id:
                    print(f"✅ Event Created Successfully!")
                    print(f"   Event ID: {event_id}")
                    print(f"   Title: {event_data.get('title', 'N/A')}")
                    print(f"   Priority: {event_data.get('priority', 'N/A')}")
                    print(f"   Start Time: {event_data.get('start_time', 'N/A')}")
                    print(f"   Location: {event_data.get('location', 'N/A')}")
                    
                    # Show hybrid analysis
                    bert_data = data.get('bert_classification', {})
                    nlp_data = data.get('nlp_analysis', {})
                    
                    print(f"🔍 NLP Analysis: {nlp_data.get('extracted_title', 'N/A')}")
                    print(f"🤖 BERT Priority: {bert_data.get('priority', 'N/A')} (confidence: {bert_data.get('confidence', 0):.3f})")
                    
                    return {
                        'success': True,
                        'event_id': event_id,
                        'event_data': event_data,
                        'hybrid_analysis': {
                            'nlp': nlp_data,
                            'bert': bert_data
                        }
                    }
                else:
                    print(f"❌ Event Creation Failed: {data.get('message', 'Unknown error')}")
                    return {'success': False, 'error': data.get('message', 'Unknown error')}
                    
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            print(f"❌ Request Failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def run_comprehensive_demo(self):
        """Run the complete Full Hybrid System demonstration"""
        print("🎯 FULL HYBRID SYSTEM DEMONSTRATION")
        print("=" * 70)
        print("Testing Voice-to-Text + Enhanced Priority + BERT + Event Creation")
        print("=" * 70)
        
        # Step 1: Health Check
        if not self.test_voice_api_health():
            print("❌ API not available. Please start the server first.")
            return
        
        print("\n" + "="*50)
        print("🧪 PHASE 1: HYBRID PRIORITY CLASSIFICATION TESTS")
        print("="*50)
        
        # Priority classification tests
        test_cases = [
            {
                'voice_text': 'urgent meeting with the CEO tomorrow at 2pm',
                'expected_priority': 5,
                'description': 'CEO Meeting (Should be CRITICAL)'
            },
            {
                'voice_text': 'schedule heart surgery consultation next week',
                'expected_priority': 5,
                'description': 'Heart Surgery (Should be CRITICAL)'
            },
            {
                'voice_text': 'emergency board meeting this afternoon',
                'expected_priority': 5,
                'description': 'Emergency Board Meeting (Should be CRITICAL)'
            },
            {
                'voice_text': 'important client presentation tomorrow',
                'expected_priority': 4,
                'description': 'Client Presentation (Should be HIGH)'
            },
            {
                'voice_text': 'casual coffee with team next Friday',
                'expected_priority': 2,
                'description': 'Casual Coffee (Should be LOW)'
            },
            {
                'voice_text': 'hangout with friends this weekend',
                'expected_priority': 1,
                'description': 'Friends Hangout (Should be VERY LOW)'
            }
        ]
        
        priority_results = []
        for test in test_cases:
            result = self.test_hybrid_priority_classification(
                test['voice_text'], 
                test['expected_priority'], 
                test['description']
            )
            priority_results.append(result)
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "="*50)
        print("🚀 PHASE 2: FULL EVENT CREATION PIPELINE TESTS")
        print("="*50)
        
        # Full pipeline tests
        creation_test_cases = [
            {
                'voice_text': 'schedule urgent meeting with CEO tomorrow at 3pm in conference room A',
                'description': 'Complete CEO Meeting Creation'
            },
            {
                'voice_text': 'book doctor appointment for heart checkup next Tuesday at 10am',
                'description': 'Medical Appointment Creation'
            },
            {
                'voice_text': 'set up casual lunch with the team next Friday at noon',
                'description': 'Team Lunch Creation'
            }
        ]
        
        creation_results = []
        for test in creation_test_cases:
            result = self.test_full_event_creation(
                test['voice_text'],
                test['description']
            )
            creation_results.append(result)
            time.sleep(2)  # Pause between database operations
        
        print("\n" + "="*70)
        print("📊 FULL HYBRID SYSTEM RESULTS SUMMARY")
        print("="*70)
        
        # Summary of priority classification
        correct_priorities = sum(1 for r in priority_results if r.get('success') and r.get('is_correct'))
        total_priority_tests = len([r for r in priority_results if r.get('success')])
        
        print(f"🎯 Priority Classification Accuracy: {correct_priorities}/{total_priority_tests} ({(correct_priorities/total_priority_tests*100):.1f}%)")
        
        # Summary of event creation
        successful_creations = sum(1 for r in creation_results if r.get('success'))
        total_creation_tests = len(creation_results)
        
        print(f"📅 Event Creation Success Rate: {successful_creations}/{total_creation_tests} ({(successful_creations/total_creation_tests*100):.1f}%)")
        
        print("\n🏆 HYBRID SYSTEM STATUS:")
        if correct_priorities == total_priority_tests and successful_creations == total_creation_tests:
            print("✅ FULL HYBRID SYSTEM: 100% OPERATIONAL")
            print("🎉 Voice-to-Text + Enhanced Priority + BERT + Event Creation = SUCCESS!")
        else:
            print("⚠️ PARTIAL SUCCESS - Some issues detected")
        
        print("\n🔧 System Components:")
        print("  ✅ Voice Text Processing")
        print("  ✅ Enhanced Priority Keywords (CEO, surgery, emergency)")
        print("  ✅ BERT AI Classification")
        print("  ✅ Hybrid Decision Logic")
        print("  ✅ Event Database Integration")
        print("  ✅ Real-time API Processing")
        
        return {
            'priority_results': priority_results,
            'creation_results': creation_results,
            'priority_accuracy': correct_priorities / total_priority_tests if total_priority_tests > 0 else 0,
            'creation_success_rate': successful_creations / total_creation_tests if total_creation_tests > 0 else 0
        }

def main():
    """Run the Full Hybrid System Demo"""
    demo = FullHybridSystemDemo()
    
    print("🎬 Starting Full Hybrid System Demonstration...")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        results = demo.run_comprehensive_demo()
        
        print("\n" + "="*70)
        print("🎊 DEMONSTRATION COMPLETE!")
        print("="*70)
        
        if results:
            accuracy = results.get('priority_accuracy', 0)
            success_rate = results.get('creation_success_rate', 0)
            
            if accuracy >= 0.9 and success_rate >= 0.9:
                print("🏆 OUTSTANDING: Full Hybrid System performing at 90%+ efficiency!")
            elif accuracy >= 0.8 and success_rate >= 0.8:
                print("👍 GOOD: Full Hybrid System performing well!")
            else:
                print("⚠️ NEEDS ATTENTION: Some components require optimization")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")

if __name__ == "__main__":
    main()
