#!/usr/bin/env python3
"""
Voice Command Demo Script for KairoCal
Demonstrates voice-to-text functionality with 20+ realistic examples
Shows voice input → event creation results with different priority levels
"""

import sys
import os
import json
import time
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VoiceCommandDemo:
    """Demonstration of voice command processing capabilities"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.voice_endpoint = f"{base_url}/api/v1/voice"
        self.test_user_id = 1
        self.demo_results = []
        
        # 20+ realistic voice command examples organized by priority level
        self.voice_commands = {
            "Critical Priority (5)": [
                "URGENT: Emergency board meeting now in the main conference room",
                "ASAP: Production server is down need all hands meeting immediately",
                "CRITICAL: CEO wants to see quarterly results right away",
                "EMERGENCY: Data breach incident response meeting in 5 minutes",
                "DROP EVERYTHING: Client threatening to cancel contract need meeting now"
            ],
            
            "High Priority (4)": [
                "Important client presentation tomorrow at 2pm in conference room A",
                "Deadline: Submit project proposal by end of day tomorrow",
                "High priority interview with senior developer candidate next Tuesday at 10am",
                "Crucial budget review meeting with CFO next Wednesday at 3pm",
                "Time sensitive call with legal team about contract terms tomorrow morning"
            ],
            
            "Medium Priority (3)": [
                "Weekly team standup meeting next Monday at 9am",
                "Doctor appointment for annual checkup next Thursday at 2:30pm",
                "Monthly project review with stakeholders next Friday at 1pm",
                "Training session on new software tools next Wednesday morning",
                "Regular one-on-one with manager next Tuesday at 4pm"
            ],
            
            "Low Priority (2)": [
                "Optional workshop on productivity techniques next week",
                "Casual team lunch at the new restaurant next Friday",
                "Nice to have meeting about office improvements sometime next month",
                "Training session on optional tools when convenient",
                "Coffee chat with new team member next week"
            ],
            
            "Very Low Priority (1)": [
                "Informal coffee break with colleagues in 30 minutes",
                "Social happy hour event next Friday evening",
                "Casual walk and talk meeting whenever works",
                "Optional company picnic next weekend",
                "Relaxed brainstorming session when people are free"
            ],
            
            "Complex Voice Commands": [
                "Um, so I need to, like, schedule a meeting with John and Sarah about the, uh, project review for next Monday at 3pm in, you know, conference room B",
                "Remind me to call the client about the deadline extension tomorrow morning around 10 or 11am",
                "Book doctor appointment with Dr. Smith for next Tuesday afternoon sometime between 2 and 4pm",
                "Schedule urgent team meeting tomorrow with all developers and QA people at 9am sharp",
                "Set up conference call with international team next Wednesday at 8am our time 2pm their time"
            ]
        }
    
    def demonstrate_voice_processing(self, voice_text: str, category: str) -> Dict[str, Any]:
        """Process a single voice command and show results"""
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🎤 Voice Command: '{voice_text}'")
        logger.info(f"📂 Category: {category}")
        
        demo_result = {
            'voice_text': voice_text,
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'processing_steps': {}
        }
        
        try:
            # Step 1: Voice Transcription and Cleaning
            logger.info(f"\n📝 Step 1: Voice Transcription & Cleaning")
            
            transcribe_data = {
                "text": voice_text,
                "user_id": self.test_user_id,
                "language": "en",
                "confidence_threshold": 0.5
            }
            
            transcribe_response = requests.post(
                f"{self.voice_endpoint}/transcribe",
                json=transcribe_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if transcribe_response.status_code == 200:
                transcribe_result = transcribe_response.json()
                
                logger.info(f"   🧹 Cleaned Text: '{transcribe_result['cleaned_text']}'")
                logger.info(f"   📊 Transcription Confidence: {transcribe_result['confidence']:.2f}")
                logger.info(f"   ⏱️ Processing Time: {transcribe_result['processing_time']:.3f}s")
                
                demo_result['processing_steps']['transcription'] = {
                    'success': True,
                    'cleaned_text': transcribe_result['cleaned_text'],
                    'confidence': transcribe_result['confidence'],
                    'processing_time': transcribe_result['processing_time'],
                    'metadata': transcribe_result['metadata']
                }
            else:
                logger.error(f"   ❌ Transcription failed: HTTP {transcribe_response.status_code}")
                demo_result['processing_steps']['transcription'] = {
                    'success': False,
                    'error': f"HTTP {transcribe_response.status_code}"
                }
                return demo_result
            
            # Step 2: Voice Analysis (without creating event)
            logger.info(f"\n🔍 Step 2: Voice Analysis & Entity Extraction")
            
            analyze_response = requests.post(
                f"{self.voice_endpoint}/analyze-voice",
                params={"voice_text": voice_text, "user_id": self.test_user_id},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if analyze_response.status_code == 200:
                analyze_result = analyze_response.json()
                
                # Display NLP analysis
                nlp_analysis = analyze_result.get('nlp_analysis', {})
                logger.info(f"   📋 Extracted Title: '{nlp_analysis.get('title', 'N/A')}'")
                logger.info(f"   📅 Detected Time: {nlp_analysis.get('start_time', 'Not detected')}")
                logger.info(f"   📍 Detected Location: '{nlp_analysis.get('location', 'None')}'")
                logger.info(f"   🏷️ Event Type: {nlp_analysis.get('event_type', 'general')}")
                logger.info(f"   👥 Participants: {nlp_analysis.get('participants', [])}")
                logger.info(f"   ⏱️ Duration: {nlp_analysis.get('duration', 60)} minutes")
                
                # Display BERT analysis
                bert_analysis = analyze_result.get('bert_analysis', {})
                logger.info(f"   🤖 BERT Priority: {bert_analysis.get('priority', 'N/A')}")
                logger.info(f"   📊 BERT Confidence: {bert_analysis.get('confidence', 0):.3f}")
                logger.info(f"   🔧 BERT Available: {'✅' if bert_analysis.get('available', False) else '❌'}")
                
                # Display recommended event
                recommended = analyze_result.get('recommended_event', {})
                logger.info(f"   💡 Recommended Event:")
                logger.info(f"      Title: '{recommended.get('title', 'N/A')}'")
                logger.info(f"      Priority: {recommended.get('priority', 'N/A')}")
                logger.info(f"      Confidence: {recommended.get('confidence', 0):.3f}")
                
                demo_result['processing_steps']['analysis'] = {
                    'success': True,
                    'nlp_analysis': nlp_analysis,
                    'bert_analysis': bert_analysis,
                    'recommended_event': recommended
                }
            else:
                logger.error(f"   ❌ Analysis failed: HTTP {analyze_response.status_code}")
                demo_result['processing_steps']['analysis'] = {
                    'success': False,
                    'error': f"HTTP {analyze_response.status_code}"
                }
            
            # Step 3: Event Creation
            logger.info(f"\n📅 Step 3: Event Creation")
            
            create_data = {
                "voice_text": voice_text,
                "user_id": self.test_user_id,
                "auto_schedule": True
            }
            
            create_response = requests.post(
                f"{self.voice_endpoint}/create-event",
                json=create_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if create_response.status_code == 200:
                create_result = create_response.json()
                
                logger.info(f"   🎯 Event Creation: {'✅ SUCCESS' if create_result['success'] else '❌ FAILED'}")
                logger.info(f"   📝 Message: {create_result['message']}")
                
                if create_result['success']:
                    logger.info(f"   🆔 Event ID: {create_result.get('event_id', 'N/A')}")
                    
                    # Event data
                    event_data = create_result.get('event_data', {})
                    logger.info(f"   📋 Event Title: '{event_data.get('title', 'N/A')}'")
                    logger.info(f"   📅 Start Time: {event_data.get('start_time', 'N/A')}")
                    logger.info(f"   📍 Location: '{event_data.get('location', 'None')}'")
                    logger.info(f"   🎯 Priority: {event_data.get('priority', 'N/A')}")
                    
                    # BERT classification details
                    bert_classification = create_result.get('bert_classification', {})
                    logger.info(f"   🤖 BERT Classification:")
                    logger.info(f"      Original Priority: {bert_classification.get('priority', 'N/A')}")
                    logger.info(f"      Confidence: {bert_classification.get('confidence', 0):.3f}")
                    logger.info(f"      Final Priority: {bert_classification.get('final_priority', 'N/A')}")
                    logger.info(f"      Model Used: {bert_classification.get('model_used', 'Unknown')}")
                    
                    # Processing details
                    processing_details = create_result.get('processing_details', {})
                    logger.info(f"   ⏱️ Total Processing Time: {processing_details.get('total_processing_time', 0):.3f}s")
                    logger.info(f"   🗑️ Words Removed: {processing_details.get('words_removed', 0)}")
                
                demo_result['processing_steps']['event_creation'] = {
                    'success': create_result['success'],
                    'event_id': create_result.get('event_id'),
                    'event_data': create_result.get('event_data', {}),
                    'bert_classification': create_result.get('bert_classification', {}),
                    'processing_details': create_result.get('processing_details', {}),
                    'message': create_result['message']
                }
            else:
                logger.error(f"   ❌ Event creation failed: HTTP {create_response.status_code}")
                demo_result['processing_steps']['event_creation'] = {
                    'success': False,
                    'error': f"HTTP {create_response.status_code}",
                    'response': create_response.text
                }
            
            # Summary
            logger.info(f"\n📊 Processing Summary:")
            transcription_success = demo_result['processing_steps'].get('transcription', {}).get('success', False)
            analysis_success = demo_result['processing_steps'].get('analysis', {}).get('success', False)
            creation_success = demo_result['processing_steps'].get('event_creation', {}).get('success', False)
            
            logger.info(f"   🎤 Transcription: {'✅' if transcription_success else '❌'}")
            logger.info(f"   🔍 Analysis: {'✅' if analysis_success else '❌'}")
            logger.info(f"   📅 Event Creation: {'✅' if creation_success else '❌'}")
            
            overall_success = transcription_success and analysis_success and creation_success
            logger.info(f"   🏆 Overall: {'✅ SUCCESS' if overall_success else '❌ FAILED'}")
            
            demo_result['overall_success'] = overall_success
            
        except requests.RequestException as e:
            logger.error(f"❌ Network error: {str(e)}")
            demo_result['error'] = f"Network error: {str(e)}"
        except Exception as e:
            logger.error(f"❌ Unexpected error: {str(e)}")
            demo_result['error'] = f"Unexpected error: {str(e)}"
        
        return demo_result
    
    def run_priority_level_demos(self):
        """Run demonstrations for each priority level"""
        logger.info("🎯 Priority Level Demonstrations")
        logger.info("=" * 80)
        
        for priority_category, commands in self.voice_commands.items():
            logger.info(f"\n🏷️ {priority_category}")
            logger.info("-" * 60)
            
            for i, command in enumerate(commands, 1):
                logger.info(f"\n[{i}/{len(commands)}] Processing command...")
                
                result = self.demonstrate_voice_processing(command, priority_category)
                self.demo_results.append(result)
                
                # Brief pause between commands
                time.sleep(1)
    
    def run_selected_demos(self, categories: List[str] = None):
        """Run demonstrations for selected categories only"""
        
        if categories is None:
            categories = list(self.voice_commands.keys())
        
        logger.info(f"🎯 Selected Voice Command Demonstrations")
        logger.info(f"📂 Categories: {', '.join(categories)}")
        logger.info("=" * 80)
        
        for category in categories:
            if category in self.voice_commands:
                commands = self.voice_commands[category]
                logger.info(f"\n🏷️ {category}")
                logger.info("-" * 60)
                
                for i, command in enumerate(commands, 1):
                    logger.info(f"\n[{i}/{len(commands)}] Processing command...")
                    
                    result = self.demonstrate_voice_processing(command, category)
                    self.demo_results.append(result)
                    
                    # Brief pause between commands
                    time.sleep(1)
            else:
                logger.warning(f"⚠️ Category '{category}' not found")
    
    def generate_demo_report(self):
        """Generate comprehensive demo report"""
        logger.info("\n📊 Voice Command Demo Report")
        logger.info("=" * 80)
        
        if not self.demo_results:
            logger.warning("⚠️ No demo results to report")
            return
        
        # Overall statistics
        total_commands = len(self.demo_results)
        successful_commands = len([r for r in self.demo_results if r.get('overall_success', False)])
        
        logger.info(f"📈 Demo Summary:")
        logger.info(f"   Total Commands Tested: {total_commands}")
        logger.info(f"   ✅ Successful: {successful_commands}")
        logger.info(f"   ❌ Failed: {total_commands - successful_commands}")
        logger.info(f"   📊 Success Rate: {(successful_commands/total_commands)*100:.1f}%")
        
        # Priority level breakdown
        priority_stats = {}
        for result in self.demo_results:
            category = result.get('category', 'Unknown')
            if category not in priority_stats:
                priority_stats[category] = {'total': 0, 'successful': 0}
            
            priority_stats[category]['total'] += 1
            if result.get('overall_success', False):
                priority_stats[category]['successful'] += 1
        
        logger.info(f"\n📋 Results by Priority Level:")
        for category, stats in priority_stats.items():
            success_rate = (stats['successful'] / stats['total']) * 100 if stats['total'] > 0 else 0
            logger.info(f"   {category}: {stats['successful']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Processing step analysis
        step_stats = {
            'transcription': {'success': 0, 'total': 0},
            'analysis': {'success': 0, 'total': 0},
            'event_creation': {'success': 0, 'total': 0}
        }
        
        for result in self.demo_results:
            steps = result.get('processing_steps', {})
            for step_name in step_stats.keys():
                if step_name in steps:
                    step_stats[step_name]['total'] += 1
                    if steps[step_name].get('success', False):
                        step_stats[step_name]['success'] += 1
        
        logger.info(f"\n🔧 Processing Step Analysis:")
        for step_name, stats in step_stats.items():
            if stats['total'] > 0:
                success_rate = (stats['success'] / stats['total']) * 100
                logger.info(f"   {step_name.title()}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # BERT performance analysis
        bert_priorities = []
        bert_confidences = []
        
        for result in self.demo_results:
            bert_data = result.get('processing_steps', {}).get('event_creation', {}).get('bert_classification', {})
            if bert_data.get('priority'):
                bert_priorities.append(bert_data['priority'])
            if bert_data.get('confidence'):
                bert_confidences.append(bert_data['confidence'])
        
        if bert_priorities:
            logger.info(f"\n🤖 BERT Performance Analysis:")
            logger.info(f"   Commands with BERT Classification: {len(bert_priorities)}/{total_commands}")
            logger.info(f"   Average Priority: {sum(bert_priorities)/len(bert_priorities):.1f}")
            if bert_confidences:
                logger.info(f"   Average Confidence: {sum(bert_confidences)/len(bert_confidences):.3f}")
                logger.info(f"   Confidence Range: {min(bert_confidences):.3f} - {max(bert_confidences):.3f}")
        
        # Save detailed report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"voice_demo_report_{timestamp}.json"
        
        detailed_report = {
            'demo_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_commands': total_commands,
                'successful_commands': successful_commands,
                'success_rate': (successful_commands/total_commands)*100,
                'priority_level_stats': priority_stats,
                'processing_step_stats': step_stats
            },
            'bert_analysis': {
                'commands_classified': len(bert_priorities),
                'average_priority': sum(bert_priorities)/len(bert_priorities) if bert_priorities else 0,
                'average_confidence': sum(bert_confidences)/len(bert_confidences) if bert_confidences else 0,
                'priority_distribution': {i: bert_priorities.count(i) for i in range(1, 6)}
            },
            'detailed_results': self.demo_results
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_report, f, indent=2, default=str)
            logger.info(f"\n💾 Detailed report saved to: {report_file}")
        except Exception as e:
            logger.error(f"⚠️ Failed to save detailed report: {e}")
        
        return detailed_report
    
    def generate_curl_commands(self):
        """Generate curl commands for manual testing"""
        logger.info("\n🌐 cURL Commands for Manual Testing")
        logger.info("=" * 80)
        
        base_url = self.voice_endpoint
        
        # Select representative commands from each priority level
        representative_commands = {
            "Critical": "URGENT: Emergency board meeting now in the main conference room",
            "High": "Important client presentation tomorrow at 2pm in conference room A",
            "Medium": "Weekly team standup meeting next Monday at 9am",
            "Low": "Optional workshop on productivity techniques next week",
            "Very Low": "Informal coffee break with colleagues in 30 minutes"
        }
        
        for priority, command in representative_commands.items():
            logger.info(f"\n🏷️ {priority} Priority Example:")
            logger.info(f"Voice Text: '{command}'")
            logger.info(f"cURL Command:")
            
            curl_command = f"""curl -X POST "{base_url}/create-event" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "voice_text": "{command}",
    "user_id": 1,
    "auto_schedule": true
  }}' \\
  | jq '.bert_classification.final_priority, .event_data.title, .message'"""
            
            logger.info(f"{curl_command}")
        
        # Additional useful commands
        logger.info(f"\n🔧 Additional Testing Commands:")
        
        logger.info(f"\n1. Health Check:")
        logger.info(f"""curl -X GET "{base_url}/health" | jq '.'""")
        
        logger.info(f"\n2. Voice Analysis (no event creation):")
        logger.info(f"""curl -X POST "{base_url}/analyze-voice" \\
  -H "Content-Type: application/json" \\
  -d "voice_text=Schedule urgent meeting tomorrow&user_id=1" \\
  | jq '.recommended_event'""")
        
        logger.info(f"\n3. Transcription Test:")
        logger.info(f"""curl -X POST "{base_url}/transcribe" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "text": "Um, like, schedule a meeting with, uh, John tomorrow",
    "user_id": 1
  }}' \\
  | jq '.cleaned_text, .confidence'""")

def main():
    """Main demo entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Voice Command Demo Script")
    parser.add_argument('--base-url', default='http://localhost:8000',
                       help='Base URL for the API (default: http://localhost:8000)')
    parser.add_argument('--categories', nargs='+',
                       choices=['Critical Priority (5)', 'High Priority (4)', 'Medium Priority (3)', 
                               'Low Priority (2)', 'Very Low Priority (1)', 'Complex Voice Commands'],
                       help='Run demo for specific categories only')
    parser.add_argument('--curl-examples', action='store_true',
                       help='Generate curl command examples')
    parser.add_argument('--quick-demo', action='store_true',
                       help='Run quick demo with one example from each priority level')
    
    args = parser.parse_args()
    
    # Initialize demo
    demo = VoiceCommandDemo(args.base_url)
    
    if args.curl_examples:
        demo.generate_curl_commands()
        return 0
    
    try:
        logger.info("🎤 KairoCal Voice Command Demonstration")
        logger.info("=" * 80)
        logger.info(f"🌐 API Base URL: {args.base_url}")
        logger.info(f"⏰ Demo Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if args.quick_demo:
            # Quick demo - one from each category
            quick_categories = ['Critical Priority (5)', 'High Priority (4)', 'Medium Priority (3)', 
                              'Low Priority (2)', 'Very Low Priority (1)']
            
            for category in quick_categories:
                if category in demo.voice_commands:
                    command = demo.voice_commands[category][0]  # Take first command
                    result = demo.demonstrate_voice_processing(command, category)
                    demo.demo_results.append(result)
                    time.sleep(1)
        
        elif args.categories:
            # Run selected categories
            demo.run_selected_demos(args.categories)
        
        else:
            # Run full demo
            demo.run_priority_level_demos()
        
        # Generate report
        if demo.demo_results:
            demo.generate_demo_report()
            demo.generate_curl_commands()
            
            logger.info("\n🎉 Voice command demonstration completed!")
            logger.info("📊 Check the generated report for detailed results")
        else:
            logger.warning("⚠️ No demo results to report")
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Demo interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Demo failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
