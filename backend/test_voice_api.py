#!/usr/bin/env python3
"""
Voice API Testing Suite for KairoCal
Comprehensive testing of voice-to-text API endpoints and integration
"""

import sys
import os
import json
import asyncio
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VoiceAPITester:
    """Comprehensive testing suite for Voice API endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.voice_endpoint = f"{base_url}/api/v1/voice"
        self.test_user_id = 1  # Assuming test user exists
        self.test_results = []
        
    def test_voice_transcribe_endpoint(self):
        """Test the voice transcription endpoint"""
        logger.info("🎤 Testing Voice Transcription Endpoint")
        logger.info("=" * 50)
        
        test_cases = [
            {
                "name": "Simple meeting request",
                "text": "Schedule a meeting with John tomorrow at 3pm",
                "expected_confidence": 0.8
            },
            {
                "name": "Urgent appointment",
                "text": "Um, I need to, uh, schedule an urgent doctor appointment for like tomorrow morning",
                "expected_confidence": 0.7
            },
            {
                "name": "Complex event with location",
                "text": "Remind me to call the client about the project deadline next Friday at 2pm in conference room A",
                "expected_confidence": 0.9
            },
            {
                "name": "Casual social event",
                "text": "Coffee with Sarah next week sometime in the afternoon",
                "expected_confidence": 0.6
            },
            {
                "name": "Voice with filler words",
                "text": "So, um, I was thinking, you know, maybe we could, like, set up a team meeting for, uh, next Tuesday",
                "expected_confidence": 0.7
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"\n📝 Test Case {i}: {test_case['name']}")
            
            # Prepare request data
            request_data = {
                "text": test_case["text"],
                "user_id": self.test_user_id,
                "language": "en",
                "confidence_threshold": 0.5
            }
            
            try:
                # Make API request
                response = requests.post(
                    f"{self.voice_endpoint}/transcribe",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    logger.info(f"   ✅ Status: SUCCESS")
                    logger.info(f"   📝 Original: '{result['transcribed_text']}'")
                    logger.info(f"   🧹 Cleaned: '{result['cleaned_text']}'")
                    logger.info(f"   📊 Confidence: {result['confidence']:.2f}")
                    logger.info(f"   ⏱️ Processing Time: {result['processing_time']:.3f}s")
                    
                    # Validate confidence
                    if result['confidence'] >= test_case['expected_confidence']:
                        logger.info(f"   ✅ Confidence meets expectation")
                    else:
                        logger.warning(f"   ⚠️ Low confidence (expected: {test_case['expected_confidence']})")
                    
                    self.test_results.append({
                        'test': test_case['name'],
                        'endpoint': 'transcribe',
                        'status': 'PASS',
                        'confidence': result['confidence'],
                        'processing_time': result['processing_time']
                    })
                    
                else:
                    logger.error(f"   ❌ Status: FAILED - HTTP {response.status_code}")
                    logger.error(f"   📄 Response: {response.text}")
                    
                    self.test_results.append({
                        'test': test_case['name'],
                        'endpoint': 'transcribe',
                        'status': 'FAIL',
                        'error': f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                logger.error(f"   ❌ Exception: {str(e)}")
                self.test_results.append({
                    'test': test_case['name'],
                    'endpoint': 'transcribe',
                    'status': 'ERROR',
                    'error': str(e)
                })
    
    def test_voice_create_event_endpoint(self):
        """Test the voice event creation endpoint"""
        logger.info("\n📅 Testing Voice Event Creation Endpoint")
        logger.info("=" * 50)
        
        test_cases = [
            {
                "name": "Urgent meeting creation",
                "voice_text": "URGENT: Schedule board meeting with CEO tomorrow at 10am in conference room A",
                "auto_schedule": True,
                "expected_priority": 5
            },
            {
                "name": "Doctor appointment",
                "voice_text": "Book doctor appointment next Wednesday at 2pm",
                "auto_schedule": True,
                "expected_priority": 3
            },
            {
                "name": "Team lunch",
                "voice_text": "Casual team lunch next Friday at noon",
                "auto_schedule": True,
                "expected_priority": 2
            },
            {
                "name": "Client call with override",
                "voice_text": "Client call tomorrow morning",
                "auto_schedule": True,
                "priority_override": 4,
                "expected_priority": 4
            },
            {
                "name": "Meeting with participants",
                "voice_text": "Meeting with John and Sarah about project review next Monday at 3pm",
                "auto_schedule": True,
                "expected_priority": 3
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"\n📝 Test Case {i}: {test_case['name']}")
            
            # Prepare request data
            request_data = {
                "voice_text": test_case["voice_text"],
                "user_id": self.test_user_id,
                "auto_schedule": test_case.get("auto_schedule", True)
            }
            
            if "priority_override" in test_case:
                request_data["priority_override"] = test_case["priority_override"]
            
            try:
                # Make API request
                response = requests.post(
                    f"{self.voice_endpoint}/create-event",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    logger.info(f"   ✅ Status: {'SUCCESS' if result['success'] else 'FAILED'}")
                    logger.info(f"   📅 Event ID: {result.get('event_id', 'N/A')}")
                    logger.info(f"   📝 Message: {result['message']}")
                    
                    # Display NLP analysis
                    nlp = result.get('nlp_analysis', {})
                    logger.info(f"   🧹 Cleaned Text: '{nlp.get('cleaned_text', '')}'")
                    logger.info(f"   📋 Title: '{nlp.get('extracted_title', '')}'")
                    logger.info(f"   📍 Location: '{nlp.get('extracted_location', 'None')}'")
                    
                    # Display BERT classification
                    bert = result.get('bert_classification', {})
                    logger.info(f"   🤖 BERT Priority: {bert.get('priority', 'N/A')}")
                    logger.info(f"   📊 BERT Confidence: {bert.get('confidence', 'N/A'):.3f}")
                    logger.info(f"   🎯 Final Priority: {bert.get('final_priority', 'N/A')}")
                    logger.info(f"   🏷️ Model Used: {bert.get('model_used', 'Unknown')}")
                    
                    # Display processing details
                    processing = result.get('processing_details', {})
                    logger.info(f"   ⏱️ Total Time: {processing.get('total_processing_time', 0):.3f}s")
                    logger.info(f"   🗑️ Words Removed: {processing.get('words_removed', 0)}")
                    
                    # Validate priority
                    final_priority = bert.get('final_priority')
                    expected_priority = test_case.get('expected_priority')
                    if final_priority == expected_priority:
                        logger.info(f"   ✅ Priority matches expectation")
                    else:
                        logger.warning(f"   ⚠️ Priority mismatch (expected: {expected_priority}, got: {final_priority})")
                    
                    self.test_results.append({
                        'test': test_case['name'],
                        'endpoint': 'create-event',
                        'status': 'PASS' if result['success'] else 'FAIL',
                        'event_id': result.get('event_id'),
                        'priority': final_priority,
                        'bert_confidence': bert.get('confidence', 0),
                        'processing_time': processing.get('total_processing_time', 0)
                    })
                    
                else:
                    logger.error(f"   ❌ Status: FAILED - HTTP {response.status_code}")
                    logger.error(f"   📄 Response: {response.text}")
                    
                    self.test_results.append({
                        'test': test_case['name'],
                        'endpoint': 'create-event',
                        'status': 'FAIL',
                        'error': f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                logger.error(f"   ❌ Exception: {str(e)}")
                self.test_results.append({
                    'test': test_case['name'],
                    'endpoint': 'create-event',
                    'status': 'ERROR',
                    'error': str(e)
                })
    
    def test_voice_analyze_endpoint(self):
        """Test the voice analysis endpoint"""
        logger.info("\n🔍 Testing Voice Analysis Endpoint")
        logger.info("=" * 50)
        
        test_cases = [
            "Schedule important client presentation for next Friday at 2pm",
            "Coffee break in 10 minutes",
            "URGENT: Emergency team meeting now",
            "Optional training workshop next week",
            "Doctor appointment tomorrow morning"
        ]
        
        for i, voice_text in enumerate(test_cases, 1):
            logger.info(f"\n📝 Test Case {i}: '{voice_text}'")
            
            try:
                # Make API request
                response = requests.post(
                    f"{self.voice_endpoint}/analyze-voice",
                    params={"voice_text": voice_text, "user_id": self.test_user_id},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    logger.info(f"   ✅ Status: SUCCESS")
                    
                    # Voice cleaning results
                    cleaning = result.get('voice_cleaning', {})
                    logger.info(f"   🧹 Cleaned: '{cleaning.get('cleaned_text', '')}'")
                    logger.info(f"   🗑️ Words Removed: {cleaning.get('removed_words', 0)}")
                    
                    # NLP analysis
                    nlp = result.get('nlp_analysis', {})
                    logger.info(f"   📋 Title: '{nlp.get('title', '')}'")
                    logger.info(f"   📅 Start Time: {nlp.get('start_time', 'Not detected')}")
                    logger.info(f"   📍 Location: '{nlp.get('location', 'None')}'")
                    logger.info(f"   🏷️ Event Type: {nlp.get('event_type', 'event')}")
                    
                    # BERT analysis
                    bert = result.get('bert_analysis', {})
                    logger.info(f"   🤖 BERT Priority: {bert.get('priority', 'N/A')}")
                    logger.info(f"   📊 BERT Confidence: {bert.get('confidence', 0):.3f}")
                    logger.info(f"   🔧 BERT Available: {bert.get('available', False)}")
                    
                    # Recommended event
                    recommended = result.get('recommended_event', {})
                    logger.info(f"   💡 Recommended Title: '{recommended.get('title', '')}'")
                    logger.info(f"   💡 Recommended Priority: {recommended.get('priority', 'N/A')}")
                    
                    self.test_results.append({
                        'test': f'analyze-{i}',
                        'endpoint': 'analyze-voice',
                        'status': 'PASS',
                        'priority': bert.get('priority'),
                        'confidence': bert.get('confidence', 0)
                    })
                    
                else:
                    logger.error(f"   ❌ Status: FAILED - HTTP {response.status_code}")
                    logger.error(f"   📄 Response: {response.text}")
                    
                    self.test_results.append({
                        'test': f'analyze-{i}',
                        'endpoint': 'analyze-voice',
                        'status': 'FAIL',
                        'error': f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                logger.error(f"   ❌ Exception: {str(e)}")
                self.test_results.append({
                    'test': f'analyze-{i}',
                    'endpoint': 'analyze-voice',
                    'status': 'ERROR',
                    'error': str(e)
                })
    
    def test_voice_health_endpoint(self):
        """Test the voice health check endpoint"""
        logger.info("\n🏥 Testing Voice Health Check Endpoint")
        logger.info("=" * 50)
        
        try:
            response = requests.get(f"{self.voice_endpoint}/health")
            
            if response.status_code == 200:
                result = response.json()
                
                logger.info(f"   ✅ Status: {result.get('status', 'unknown')}")
                logger.info(f"   ⏰ Timestamp: {result.get('timestamp', 'unknown')}")
                logger.info(f"   🔢 Version: {result.get('version', 'unknown')}")
                
                services = result.get('services', {})
                logger.info(f"   🎤 Voice Processor: {services.get('voice_processor', 'unknown')}")
                logger.info(f"   🧠 NLP Service: {services.get('nlp_service', 'unknown')}")
                logger.info(f"   🤖 BERT Model: {services.get('bert_model', 'unknown')}")
                
                self.test_results.append({
                    'test': 'health-check',
                    'endpoint': 'health',
                    'status': 'PASS',
                    'services': services
                })
                
            else:
                logger.error(f"   ❌ Status: FAILED - HTTP {response.status_code}")
                self.test_results.append({
                    'test': 'health-check',
                    'endpoint': 'health',
                    'status': 'FAIL',
                    'error': f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            logger.error(f"   ❌ Exception: {str(e)}")
            self.test_results.append({
                'test': 'health-check',
                'endpoint': 'health',
                'status': 'ERROR',
                'error': str(e)
            })
    
    def test_full_pipeline(self):
        """Test the complete voice → NLP → BERT → database pipeline"""
        logger.info("\n🔄 Testing Full Voice Pipeline")
        logger.info("=" * 50)
        
        pipeline_tests = [
            {
                "name": "High Priority Meeting",
                "voice_input": "Schedule urgent board meeting with all directors tomorrow at 9am in the main conference room",
                "expected_elements": {
                    "title_keywords": ["board", "meeting"],
                    "priority_range": [4, 5],
                    "time_detected": True,
                    "location_detected": True
                }
            },
            {
                "name": "Medical Appointment",
                "voice_input": "Book doctor appointment for annual checkup next Tuesday at 2:30pm",
                "expected_elements": {
                    "title_keywords": ["doctor", "appointment"],
                    "priority_range": [2, 4],
                    "time_detected": True,
                    "location_detected": False
                }
            },
            {
                "name": "Social Event",
                "voice_input": "Casual coffee with friends next weekend",
                "expected_elements": {
                    "title_keywords": ["coffee"],
                    "priority_range": [1, 2],
                    "time_detected": False,
                    "location_detected": False
                }
            }
        ]
        
        for i, test in enumerate(pipeline_tests, 1):
            logger.info(f"\n🧪 Pipeline Test {i}: {test['name']}")
            logger.info(f"   🎤 Input: '{test['voice_input']}'")
            
            try:
                # Step 1: Transcribe
                transcribe_data = {
                    "text": test["voice_input"],
                    "user_id": self.test_user_id
                }
                
                transcribe_response = requests.post(
                    f"{self.voice_endpoint}/transcribe",
                    json=transcribe_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if transcribe_response.status_code != 200:
                    logger.error(f"   ❌ Transcription failed: {transcribe_response.status_code}")
                    continue
                
                transcribe_result = transcribe_response.json()
                cleaned_text = transcribe_result["cleaned_text"]
                
                logger.info(f"   🧹 Cleaned: '{cleaned_text}'")
                
                # Step 2: Create Event
                create_data = {
                    "voice_text": test["voice_input"],
                    "user_id": self.test_user_id,
                    "auto_schedule": True
                }
                
                create_response = requests.post(
                    f"{self.voice_endpoint}/create-event",
                    json=create_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if create_response.status_code != 200:
                    logger.error(f"   ❌ Event creation failed: {create_response.status_code}")
                    continue
                
                create_result = create_response.json()
                
                # Validate results
                expectations = test["expected_elements"]
                validation_results = []
                
                # Check title keywords
                title = create_result.get("nlp_analysis", {}).get("extracted_title", "").lower()
                title_match = any(keyword in title for keyword in expectations["title_keywords"])
                validation_results.append(("Title Keywords", title_match))
                
                # Check priority range
                priority = create_result.get("bert_classification", {}).get("final_priority", 0)
                priority_range = expectations["priority_range"]
                priority_match = priority_range[0] <= priority <= priority_range[1]
                validation_results.append(("Priority Range", priority_match))
                
                # Check time detection
                time_detected = create_result.get("nlp_analysis", {}).get("extracted_time") is not None
                time_match = time_detected == expectations["time_detected"]
                validation_results.append(("Time Detection", time_match))
                
                # Check location detection
                location_detected = bool(create_result.get("nlp_analysis", {}).get("extracted_location"))
                location_match = location_detected == expectations["location_detected"]
                validation_results.append(("Location Detection", location_match))
                
                # Display validation results
                logger.info(f"   📊 Validation Results:")
                all_passed = True
                for check_name, passed in validation_results:
                    status = "✅ PASS" if passed else "❌ FAIL"
                    logger.info(f"      {check_name}: {status}")
                    if not passed:
                        all_passed = False
                
                # Display key results
                logger.info(f"   📋 Extracted Title: '{title}'")
                logger.info(f"   🎯 Final Priority: {priority}")
                logger.info(f"   📅 Event Created: {'✅' if create_result['success'] else '❌'}")
                
                pipeline_status = "PASS" if all_passed and create_result['success'] else "FAIL"
                logger.info(f"   🏆 Pipeline Status: {pipeline_status}")
                
                self.test_results.append({
                    'test': test['name'],
                    'endpoint': 'full-pipeline',
                    'status': pipeline_status,
                    'event_created': create_result['success'],
                    'priority': priority,
                    'validations': validation_results
                })
                
            except Exception as e:
                logger.error(f"   ❌ Pipeline Exception: {str(e)}")
                self.test_results.append({
                    'test': test['name'],
                    'endpoint': 'full-pipeline',
                    'status': 'ERROR',
                    'error': str(e)
                })
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("\n📊 Voice API Test Report")
        logger.info("=" * 80)
        
        # Count results by status
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        error_tests = len([r for r in self.test_results if r['status'] == 'ERROR'])
        
        logger.info(f"📈 Test Summary:")
        logger.info(f"   Total Tests: {total_tests}")
        logger.info(f"   ✅ Passed: {passed_tests}")
        logger.info(f"   ❌ Failed: {failed_tests}")
        logger.info(f"   🚨 Errors: {error_tests}")
        logger.info(f"   📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Group by endpoint
        endpoint_results = {}
        for result in self.test_results:
            endpoint = result['endpoint']
            if endpoint not in endpoint_results:
                endpoint_results[endpoint] = []
            endpoint_results[endpoint].append(result)
        
        logger.info(f"\n📋 Results by Endpoint:")
        for endpoint, results in endpoint_results.items():
            passed = len([r for r in results if r['status'] == 'PASS'])
            total = len(results)
            logger.info(f"   {endpoint}: {passed}/{total} passed ({(passed/total)*100:.1f}%)")
        
        # Save detailed report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"voice_api_test_report_{timestamp}.json"
        
        detailed_report = {
            'test_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'errors': error_tests,
                'success_rate': (passed_tests/total_tests)*100
            },
            'endpoint_summary': {
                endpoint: {
                    'total': len(results),
                    'passed': len([r for r in results if r['status'] == 'PASS']),
                    'success_rate': (len([r for r in results if r['status'] == 'PASS'])/len(results))*100
                }
                for endpoint, results in endpoint_results.items()
            },
            'detailed_results': self.test_results
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_report, f, indent=2, default=str)
            logger.info(f"\n💾 Detailed report saved to: {report_file}")
        except Exception as e:
            logger.error(f"⚠️ Failed to save detailed report: {e}")
        
        return detailed_report
    
    def run_all_tests(self):
        """Run complete test suite"""
        logger.info("🧪 Starting Voice API Test Suite")
        logger.info("=" * 80)
        
        # Run all test categories
        self.test_voice_health_endpoint()
        self.test_voice_transcribe_endpoint()
        self.test_voice_analyze_endpoint()
        self.test_voice_create_event_endpoint()
        self.test_full_pipeline()
        
        # Generate report
        report = self.generate_test_report()
        
        return report

def generate_curl_examples():
    """Generate curl command examples for manual testing"""
    logger.info("\n🌐 cURL Command Examples for Manual Testing")
    logger.info("=" * 80)
    
    base_url = "http://localhost:8000/api/v1/voice"
    
    examples = [
        {
            "name": "Health Check",
            "description": "Check if voice API is running",
            "command": f"""curl -X GET "{base_url}/health" \\
  -H "Content-Type: application/json" \\
  | jq '.'"""
        },
        {
            "name": "Voice Transcription",
            "description": "Test voice text cleaning and transcription",
            "command": f"""curl -X POST "{base_url}/transcribe" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "text": "Um, schedule a meeting with John tomorrow at 3pm",
    "user_id": 1,
    "language": "en",
    "confidence_threshold": 0.5
  }}' \\
  | jq '.'"""
        },
        {
            "name": "Voice Analysis",
            "description": "Analyze voice input without creating event",
            "command": f"""curl -X POST "{base_url}/analyze-voice" \\
  -H "Content-Type: application/json" \\
  -d "voice_text=Schedule urgent board meeting tomorrow at 10am&user_id=1" \\
  | jq '.'"""
        },
        {
            "name": "Create Event from Voice",
            "description": "Full pipeline: voice → event creation",
            "command": f"""curl -X POST "{base_url}/create-event" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "voice_text": "URGENT: Client presentation deadline tomorrow at 2pm in conference room A",
    "user_id": 1,
    "auto_schedule": true
  }}' \\
  | jq '.'"""
        },
        {
            "name": "Create Event with Priority Override",
            "description": "Create event with manual priority setting",
            "command": f"""curl -X POST "{base_url}/create-event" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "voice_text": "Team lunch next Friday",
    "user_id": 1,
    "auto_schedule": true,
    "priority_override": 4
  }}' \\
  | jq '.'"""
        }
    ]
    
    for i, example in enumerate(examples, 1):
        logger.info(f"\n{i}. {example['name']}")
        logger.info(f"   Description: {example['description']}")
        logger.info(f"   Command:")
        logger.info(f"   {example['command']}")

def main():
    """Main testing entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Voice API Testing Suite")
    parser.add_argument('--base-url', default='http://localhost:8000', 
                       help='Base URL for the API (default: http://localhost:8000)')
    parser.add_argument('--curl-examples', action='store_true',
                       help='Generate curl command examples')
    parser.add_argument('--test-only', choices=['health', 'transcribe', 'analyze', 'create-event', 'pipeline'],
                       help='Run only specific test category')
    
    args = parser.parse_args()
    
    if args.curl_examples:
        generate_curl_examples()
        return
    
    # Initialize tester
    tester = VoiceAPITester(args.base_url)
    
    try:
        if args.test_only:
            if args.test_only == 'health':
                tester.test_voice_health_endpoint()
            elif args.test_only == 'transcribe':
                tester.test_voice_transcribe_endpoint()
            elif args.test_only == 'analyze':
                tester.test_voice_analyze_endpoint()
            elif args.test_only == 'create-event':
                tester.test_voice_create_event_endpoint()
            elif args.test_only == 'pipeline':
                tester.test_full_pipeline()
        else:
            # Run all tests
            tester.run_all_tests()
        
        # Generate final report
        if tester.test_results:
            tester.generate_test_report()
            logger.info("\n🎉 Voice API testing completed!")
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Testing interrupted by user")
    except Exception as e:
        logger.error(f"❌ Testing failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
