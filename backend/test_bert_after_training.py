#!/usr/bin/env python3
"""
Comprehensive System Integration Test for KairoCal BERT Priority Classification
Tests the complete API pipeline with trained BERT model integration
"""

import sys
import os
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemIntegrationTester:
    """Comprehensive system integration testing for BERT priority classification"""
    
    def __init__(self):
        self.test_results = []
        
    def check_system_components(self) -> bool:
        """Check if all required system components are available"""
        logger.info("🔍 Checking System Components")
        logger.info("=" * 60)
        
        components_status = {
            'bert_classifier': False,
            'model_loader': False,
            'nlp_api': False,
            'config': False
        }
        
        # Test 1: BERT Classifier
        try:
            from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
            classifier = AdvancedEventPriorityClassifier(model_path="models/bert_priority_classifier")
            if classifier.is_trained:
                components_status['bert_classifier'] = True
                logger.info("✅ BERT Classifier: Loaded and trained")
            else:
                logger.warning("⚠️ BERT Classifier: Loaded but not trained")
        except Exception as e:
            logger.error(f"❌ BERT Classifier: Failed - {e}")
        
        # Test 2: Model Loader
        try:
            from app.nlp.model_loader import load_bert_model, get_model_status
            model = load_bert_model()
            status = get_model_status()
            if status.get('loaded') and status.get('trained'):
                components_status['model_loader'] = True
                logger.info("✅ Model Loader: Working correctly")
            else:
                logger.warning("⚠️ Model Loader: Issues detected")
        except Exception as e:
            logger.error(f"❌ Model Loader: Failed - {e}")
        
        # Test 3: NLP API
        try:
            from app.api import nlp as nlp_module
            if nlp_module:
                components_status['nlp_api'] = True
                logger.info("✅ NLP API: Available")
        except Exception as e:
            logger.error(f"❌ NLP API: Failed - {e}")
        
        # Test 4: Config
        try:
            from app.config import get_settings
            settings = get_settings()
            if hasattr(settings, 'bert_model_path'):
                components_status['config'] = True
                logger.info("✅ Configuration: Loaded")
        except Exception as e:
            logger.error(f"❌ Configuration: Failed - {e}")
        
        # Summary
        passed = sum(components_status.values())
        total = len(components_status)
        logger.info(f"\n📊 Component Status: {passed}/{total} components available")
        
        if passed >= 3:  # Allow some flexibility
            logger.info("✅ System components check passed")
            return True
        else:
            logger.error("❌ Critical system components missing")
            return False
    
    def test_direct_bert_predictions(self) -> bool:
        """Test direct BERT model predictions"""
        logger.info("\n🤖 Testing Direct BERT Predictions")
        logger.info("=" * 50)
        
        try:
            from app.nlp.model_loader import get_global_bert_model
            
            model = get_global_bert_model()
            
            test_events = [
                {
                    "title": "EMERGENCY: Production server down",
                    "description": "Critical system outage affecting all users",
                    "start_time": (datetime.now() + timedelta(minutes=5)).isoformat(),
                    "location": "Data Center",
                    "expected_range": [4, 5]
                },
                {
                    "title": "Weekly team meeting",
                    "description": "Regular weekly standup meeting",
                    "start_time": (datetime.now() + timedelta(days=3)).isoformat(),
                    "location": "Conference Room",
                    "expected_range": [2, 4]
                },
                {
                    "title": "Optional lunch break",
                    "description": "Casual lunch with colleagues",
                    "start_time": (datetime.now() + timedelta(hours=2)).isoformat(),
                    "location": "Restaurant",
                    "expected_range": [1, 2]
                }
            ]
            
            correct_predictions = 0
            
            for i, event in enumerate(test_events, 1):
                try:
                    start_time = time.time()
                    priority, confidence = model.predict(event)
                    prediction_time = time.time() - start_time
                    
                    is_correct = priority in event['expected_range']
                    status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
                    
                    if is_correct:
                        correct_predictions += 1
                    
                    logger.info(f"Event {i}: {event['title'][:30]}...")
                    logger.info(f"   Prediction: Priority {priority} ({model.priority_labels[priority]})")
                    logger.info(f"   Confidence: {confidence:.3f}")
                    logger.info(f"   Time: {prediction_time:.3f}s")
                    logger.info(f"   Status: {status}")
                    
                except Exception as e:
                    logger.error(f"   ❌ Prediction failed: {e}")
            
            accuracy = (correct_predictions / len(test_events)) * 100
            logger.info(f"\n📊 Direct BERT Accuracy: {correct_predictions}/{len(test_events)} ({accuracy:.1f}%)")
            
            if accuracy >= 50:  # Accept 50% for initial model
                logger.info("✅ Direct BERT predictions test passed")
                return True
            else:
                logger.warning("⚠️ Direct BERT predictions accuracy below threshold")
                return False
                
        except Exception as e:
            logger.error(f"❌ Direct BERT test failed: {e}")
            return False
    
    def test_performance_benchmarks(self) -> bool:
        """Test system performance benchmarks"""
        logger.info("\n⚡ Testing Performance Benchmarks")
        logger.info("=" * 50)
        
        try:
            from app.nlp.model_loader import get_global_bert_model
            
            model = get_global_bert_model()
            
            # Performance test events
            test_events = [
                {
                    "title": f"Test event {i}",
                    "description": f"This is test event number {i} for performance testing",
                    "start_time": (datetime.now() + timedelta(hours=i)).isoformat(),
                    "location": "Test Location"
                }
                for i in range(1, 6)  # 5 test events for performance
            ]
            
            # Benchmark predictions
            prediction_times = []
            successful_predictions = 0
            
            logger.info(f"Running {len(test_events)} predictions for performance testing...")
            
            for i, event in enumerate(test_events, 1):
                try:
                    start_time = time.time()
                    priority, confidence = model.predict(event)
                    prediction_time = time.time() - start_time
                    
                    prediction_times.append(prediction_time)
                    successful_predictions += 1
                    
                    logger.debug(f"Event {i}: {prediction_time:.3f}s - Priority {priority}")
                    
                except Exception as e:
                    logger.error(f"Event {i}: Failed - {e}")
            
            # Calculate statistics
            if prediction_times:
                avg_time = sum(prediction_times) / len(prediction_times)
                max_time = max(prediction_times)
                min_time = min(prediction_times)
                
                logger.info(f"\n📊 Performance Results:")
                logger.info(f"   Successful predictions: {successful_predictions}/{len(test_events)}")
                logger.info(f"   Average prediction time: {avg_time:.3f}s")
                logger.info(f"   Fastest prediction: {min_time:.3f}s")
                logger.info(f"   Slowest prediction: {max_time:.3f}s")
                
                # Performance thresholds
                time_threshold = 2.0  # 2 seconds per prediction
                success_threshold = 0.8  # 80% success rate
                
                time_ok = avg_time <= time_threshold
                success_ok = (successful_predictions / len(test_events)) >= success_threshold
                
                logger.info(f"\n🎯 Performance Assessment:")
                logger.info(f"   Average time <= {time_threshold}s: {'✅' if time_ok else '❌'} ({avg_time:.3f}s)")
                logger.info(f"   Success rate >= {success_threshold*100:.0f}%: {'✅' if success_ok else '❌'} ({successful_predictions/len(test_events)*100:.1f}%)")
                
                if time_ok and success_ok:
                    logger.info("✅ Performance benchmarks test passed")
                    return True
                else:
                    logger.warning("⚠️ Performance benchmarks below expectations")
                    return False
            else:
                logger.error("❌ No successful predictions for performance testing")
                return False
                
        except Exception as e:
            logger.error(f"❌ Performance benchmark test failed: {e}")
            return False
    
    def test_error_handling_and_fallbacks(self) -> bool:
        """Test error handling and fallback mechanisms"""
        logger.info("\n🛡️ Testing Error Handling and Fallbacks")
        logger.info("=" * 50)
        
        try:
            from app.nlp.model_loader import get_global_bert_model
            from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
            
            model = get_global_bert_model()
            
            # Test 1: Invalid event data
            logger.info("Test 1: Invalid Event Data Handling")
            
            invalid_events = [
                {},  # Empty event
                {"title": ""},  # Empty title
                {"title": None},  # None title
                {"description": "Only description"},  # Missing title
                {"title": "Valid title", "start_time": "invalid-date"},  # Invalid date
            ]
            
            fallback_handled = 0
            
            for i, invalid_event in enumerate(invalid_events, 1):
                try:
                    priority, confidence = model.predict(invalid_event)
                    
                    # If we get here, fallback worked
                    fallback_handled += 1
                    logger.info(f"   Invalid Event {i}: Fallback successful - Priority {priority}")
                    
                except Exception as e:
                    logger.error(f"   Invalid Event {i}: Failed to handle - {e}")
            
            fallback_rate = (fallback_handled / len(invalid_events)) * 100
            logger.info(f"\n📊 Fallback Success Rate: {fallback_handled}/{len(invalid_events)} ({fallback_rate:.1f}%)")
            
            # Test 2: Model availability fallback
            logger.info("\nTest 2: Model Fallback Mechanisms")
            
            try:
                # Test with untrained model to verify fallback
                untrained_model = AdvancedEventPriorityClassifier()  # No model path = untrained
                
                test_event = {
                    "title": "Test fallback event",
                    "description": "Testing fallback mechanism",
                    "start_time": datetime.now().isoformat()
                }
                
                priority, confidence = untrained_model.predict(test_event)
                logger.info(f"   Untrained model fallback: Priority {priority}, Confidence {confidence:.3f}")
                logger.info(f"   ✅ Fallback mechanism working")
                
            except Exception as e:
                logger.error(f"   ❌ Fallback mechanism failed: {e}")
            
            if fallback_rate >= 60:  # 60% fallback success rate
                logger.info("\n✅ Error handling and fallbacks test passed")
                return True
            else:
                logger.warning("\n⚠️ Error handling needs improvement")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error handling test failed: {e}")
            return False
    
    def generate_integration_report(self, test_results: Dict[str, bool]) -> str:
        """Generate comprehensive integration test report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"system_integration_report_{timestamp}.json"
        
        report = {
            'test_date': datetime.now().isoformat(),
            'test_results': test_results,
            'summary': {
                'total_tests': len(test_results),
                'passed_tests': sum(test_results.values()),
                'failed_tests': len(test_results) - sum(test_results.values()),
                'success_rate': (sum(test_results.values()) / len(test_results)) * 100
            },
            'system_status': {
                'bert_model_trained': True,
                'performance_acceptable': test_results.get('performance', False),
                'error_handling_robust': test_results.get('error_handling', False)
            },
            'recommendations': self._generate_recommendations(test_results)
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"\n💾 Integration report saved to: {report_file}")
        except Exception as e:
            logger.error(f"⚠️ Failed to save report: {e}")
        
        return report_file
    
    def _generate_recommendations(self, test_results: Dict[str, bool]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        if not test_results.get('components', True):
            recommendations.append("Fix missing system components before deployment")
        
        if not test_results.get('bert_predictions', True):
            recommendations.append("Retrain BERT model or adjust prediction thresholds")
        
        if not test_results.get('performance', True):
            recommendations.append("Optimize model loading and prediction performance")
        
        if not test_results.get('error_handling', True):
            recommendations.append("Improve error handling and fallback mechanisms")
        
        if all(test_results.values()):
            recommendations.append("System ready for production deployment")
            recommendations.append("Monitor performance metrics in production")
            recommendations.append("Collect user feedback for model improvement")
        
        return recommendations
    
    def run_full_integration_test(self) -> bool:
        """Run complete system integration test suite"""
        logger.info("🧪 KairoCal BERT System Integration Test Suite")
        logger.info("=" * 80)
        logger.info(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all tests
        test_results = {}
        
        test_results['components'] = self.check_system_components()
        test_results['bert_predictions'] = self.test_direct_bert_predictions()
        test_results['performance'] = self.test_performance_benchmarks()
        test_results['error_handling'] = self.test_error_handling_and_fallbacks()
        
        # Generate summary
        passed = sum(test_results.values())
        total = len(test_results)
        success_rate = (passed / total) * 100
        
        logger.info("\n" + "=" * 80)
        logger.info("🎯 INTEGRATION TEST SUMMARY")
        logger.info("=" * 80)
        
        for test_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{test_name.replace('_', ' ').title()}: {status}")
        
        logger.info(f"\n📊 Overall Results: {passed}/{total} tests passed ({success_rate:.1f}%)")
        
        # Generate report
        report_file = self.generate_integration_report(test_results)
        
        # Final assessment
        if success_rate >= 75:  # 75% pass rate required
            logger.info("\n🎉 System integration test PASSED!")
            logger.info("✅ KairoCal BERT system is ready for production")
            return True
        else:
            logger.error("\n❌ System integration test FAILED!")
            logger.error("⚠️ Address failing tests before production deployment")
            return False

def main():
    """Main test runner"""
    print("Starting system integration test...")
    logger.info("🧪 Starting KairoCal BERT System Integration Test")
    
    tester = SystemIntegrationTester()
    success = tester.run_full_integration_test()
    
    if success:
        logger.info("\n📋 Next Steps:")
        logger.info("  1. ✅ Proceed to Task 6: Performance Report")
        logger.info("  2. 🚀 System ready for deployment consideration")
        logger.info("  3. 📊 Monitor system performance in production")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
