#!/usr/bin/env python3
"""
Final Integration Testing for KairoCal BERT Priority Classification System
Comprehensive end-to-end validation of the complete integrated system

This script performs:
✅ End-to-End Event Pipeline Testing
✅ BERT Priority Classification Integration Testing
✅ Conflict Detection with Priority Resolution Testing
✅ Analytics Endpoints Integration Testing
✅ Demo Data Generation and Validation Testing
✅ Production Readiness Final Validation
✅ Performance and Load Testing
✅ Complete System Health Check

Usage:
    python final_integration_test.py --full-test
    python final_integration_test.py --performance-test
    python final_integration_test.py --api-url http://localhost:8000
"""

import argparse
import asyncio
import sys
import os
import json
import logging
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import requests
from dataclasses import dataclass
import statistics
import concurrent.futures
import threading

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class IntegrationTestResult:
    """Result of an integration test"""
    test_name: str
    status: str  # "PASS", "FAIL", "WARNING"
    message: str
    execution_time: float
    details: Optional[Dict] = None
    error: Optional[str] = None

class FinalIntegrationTester:
    """Comprehensive final integration testing suite"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000", verbose: bool = False):
        self.api_base_url = api_base_url
        self.verbose = verbose
        self.results: List[IntegrationTestResult] = []
        self.start_time = time.time()
        self.demo_user_id = "integration-test-user"
        
    def log_result(self, result: IntegrationTestResult):
        """Log and store test result"""
        self.results.append(result)
        
        # Color coding
        color_map = {
            "PASS": "\033[92m",  # Green
            "FAIL": "\033[91m",  # Red
            "WARNING": "\033[93m"  # Yellow
        }
        reset_color = "\033[0m"
        
        status_colored = f"{color_map.get(result.status, '')}{result.status}{reset_color}"
        print(f"  {status_colored:15} {result.test_name:50} {result.message} ({result.execution_time:.3f}s)")
        
        if self.verbose and result.details:
            for key, value in result.details.items():
                print(f"    {key}: {value}")
        
        if result.error and result.status == "FAIL":
            print(f"    ERROR: {result.error}")
    
    def run_test(self, test_name: str, test_func, *args, **kwargs) -> IntegrationTestResult:
        """Run a single integration test with error handling"""
        start_time = time.time()
        
        try:
            status, message, details = test_func(*args, **kwargs)
            result = IntegrationTestResult(
                test_name=test_name,
                status=status,
                message=message,
                execution_time=time.time() - start_time,
                details=details
            )
        except Exception as e:
            result = IntegrationTestResult(
                test_name=test_name,
                status="FAIL",
                message=f"Test failed with exception",
                execution_time=time.time() - start_time,
                error=str(e),
                details={"exception": str(e), "traceback": traceback.format_exc()}
            )
        
        self.log_result(result)
        return result
    
    # Test 1: End-to-End Event Pipeline
    
    def test_event_creation_with_bert_priority(self) -> Tuple[str, str, Dict]:
        """Test complete event creation pipeline with BERT priority classification"""
        try:
            # Test high-priority event
            high_priority_event = {
                "title": "Emergency Board Meeting - System Outage",
                "description": "Critical emergency meeting to address major production system outage affecting all customers. Revenue impact estimated at $50k per hour.",
                "start_time": (datetime.now() + timedelta(hours=2)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=4)).isoformat(),
                "location": "Emergency Response Center"
            }
            
            response = requests.post(
                f"{self.api_base_url}/api/v1/events?cognito_sub={self.demo_user_id}&auto_classify_priority=true",
                json=high_priority_event,
                timeout=10
            )
            
            if response.status_code == 201:
                event_data = response.json()
                
                # Validate BERT classification
                if event_data.get('priority_level') in [1, 2]:  # Should be high priority
                    if event_data.get('classification_method') == 'bert':
                        return "PASS", f"Event created with BERT priority {event_data['priority_level']} (confidence: {event_data.get('priority_confidence', 0):.3f})", {
                            "event_id": event_data.get('id'),
                            "priority": event_data.get('priority_level'),
                            "confidence": event_data.get('priority_confidence'),
                            "method": event_data.get('classification_method')
                        }
                    else:
                        return "WARNING", f"Event created but used fallback classification method: {event_data.get('classification_method')}", event_data
                else:
                    return "FAIL", f"BERT misclassified emergency event as priority {event_data.get('priority_level')}", event_data
            else:
                return "FAIL", f"Event creation failed with status {response.status_code}", {"response": response.text}
                
        except Exception as e:
            return "FAIL", f"Event creation test failed: {str(e)}", {"error": str(e)}
    
    def test_priority_based_event_filtering(self) -> Tuple[str, str, Dict]:
        """Test priority-based event filtering and retrieval"""
        try:
            # Create events with different priorities first
            test_events = [
                {
                    "title": "Critical Security Incident",
                    "description": "Immediate security breach requiring emergency response",
                    "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
                    "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
                    "priority_level": 1
                },
                {
                    "title": "Coffee Chat with Colleague",
                    "description": "Informal catch-up over coffee",
                    "start_time": (datetime.now() + timedelta(hours=3)).isoformat(),
                    "end_time": (datetime.now() + timedelta(hours=3.5)).isoformat(),
                    "priority_level": 4
                }
            ]
            
            created_events = []
            for event in test_events:
                response = requests.post(
                    f"{self.api_base_url}/api/v1/events?cognito_sub={self.demo_user_id}&auto_classify_priority=false",
                    json=event,
                    timeout=10
                )
                if response.status_code == 201:
                    created_events.append(response.json())
            
            # Test high-priority filtering
            response = requests.get(
                f"{self.api_base_url}/api/v1/events/priority/high-priority?cognito_sub={self.demo_user_id}&max_priority=2",
                timeout=10
            )
            
            if response.status_code == 200:
                high_priority_events = response.json()
                critical_count = len([e for e in high_priority_events if e.get('priority_level') <= 2])
                
                if critical_count > 0:
                    return "PASS", f"Priority filtering successful: {critical_count} high-priority events found", {
                        "high_priority_count": critical_count,
                        "total_events": len(created_events),
                        "sample_event": high_priority_events[0] if high_priority_events else None
                    }
                else:
                    return "WARNING", "No high-priority events found in filter test", {"events_created": len(created_events)}
            else:
                return "FAIL", f"Priority filtering failed with status {response.status_code}", {"response": response.text}
                
        except Exception as e:
            return "FAIL", f"Priority filtering test failed: {str(e)}", {"error": str(e)}
    
    # Test 2: BERT Classification Integration
    
    def test_bert_nlp_endpoint(self) -> Tuple[str, str, Dict]:
        """Test BERT NLP classification endpoint"""
        try:
            test_cases = [
                {
                    "input": {
                        "title": "Production Server Down - All Customers Affected",
                        "description": "Critical production infrastructure failure causing complete service outage. Revenue loss estimated at $100k per hour.",
                        "location": "Data Center"
                    },
                    "expected_priority_range": [1, 2]  # Should be critical/high
                },
                {
                    "input": {
                        "title": "Team Lunch at Local Restaurant",
                        "description": "Optional team bonding lunch at the new Italian restaurant downtown.",
                        "location": "Restaurant"
                    },
                    "expected_priority_range": [4, 5]  # Should be low priority
                }
            ]
            
            test_results = []
            
            for i, test_case in enumerate(test_cases):
                response = requests.post(
                    f"{self.api_base_url}/api/v1/nlp/classify-priority",
                    json=test_case["input"],
                    timeout=10
                )
                
                if response.status_code == 200:
                    classification = response.json()
                    priority = classification.get('priority')
                    confidence = classification.get('confidence', 0)
                    method = classification.get('method')
                    
                    if priority in test_case["expected_priority_range"]:
                        test_results.append({
                            "test": i+1,
                            "status": "PASS",
                            "priority": priority,
                            "confidence": confidence,
                            "method": method
                        })
                    else:
                        test_results.append({
                            "test": i+1,
                            "status": "FAIL",
                            "priority": priority,
                            "expected": test_case["expected_priority_range"],
                            "confidence": confidence,
                            "method": method
                        })
                else:
                    test_results.append({
                        "test": i+1,
                        "status": "FAIL",
                        "error": f"HTTP {response.status_code}: {response.text}"
                    })
            
            passed_tests = len([r for r in test_results if r.get("status") == "PASS"])
            total_tests = len(test_results)
            
            if passed_tests == total_tests:
                avg_confidence = statistics.mean([r.get("confidence", 0) for r in test_results if "confidence" in r])
                return "PASS", f"All {total_tests} BERT classification tests passed (avg confidence: {avg_confidence:.3f})", {
                    "test_results": test_results,
                    "average_confidence": avg_confidence
                }
            elif passed_tests > 0:
                return "WARNING", f"{passed_tests}/{total_tests} BERT classification tests passed", {"test_results": test_results}
            else:
                return "FAIL", f"All {total_tests} BERT classification tests failed", {"test_results": test_results}
                
        except Exception as e:
            return "FAIL", f"BERT NLP endpoint test failed: {str(e)}", {"error": str(e)}
    
    def test_model_status_endpoint(self) -> Tuple[str, str, Dict]:
        """Test BERT model status endpoint"""
        try:
            response = requests.get(f"{self.api_base_url}/api/v1/nlp/model-status", timeout=10)
            
            if response.status_code == 200:
                status_data = response.json()
                model_status = status_data.get('status')
                
                if model_status == 'bert_loaded':
                    return "PASS", "BERT model loaded and operational", status_data
                elif model_status == 'fallback':
                    return "WARNING", "Using fallback classification (BERT not available)", status_data
                else:
                    return "FAIL", f"Model status indicates error: {model_status}", status_data
            else:
                return "FAIL", f"Model status endpoint failed with status {response.status_code}", {"response": response.text}
                
        except Exception as e:
            return "FAIL", f"Model status test failed: {str(e)}", {"error": str(e)}
    
    # Test 3: Conflict Detection Integration
    
    def test_priority_conflict_detection(self) -> Tuple[str, str, Dict]:
        """Test priority-based conflict detection"""
        try:
            # Create overlapping events with different priorities
            base_time = datetime.now() + timedelta(hours=5)
            
            conflict_events = [
                {
                    "title": "Critical Client Emergency Call",
                    "description": "Emergency call with largest client regarding contract issues",
                    "start_time": base_time.isoformat(),
                    "end_time": (base_time + timedelta(hours=2)).isoformat(),
                    "location": "Conference Room A",
                    "priority_level": 1
                },
                {
                    "title": "Casual Team Coffee Break",
                    "description": "Optional coffee break with team members",
                    "start_time": (base_time + timedelta(hours=1)).isoformat(),
                    "end_time": (base_time + timedelta(hours=2)).isoformat(),
                    "location": "Kitchen",
                    "priority_level": 4
                }
            ]
            
            # Create the conflicting events
            created_events = []
            for event in conflict_events:
                response = requests.post(
                    f"{self.api_base_url}/api/v1/events?cognito_sub={self.demo_user_id}&auto_classify_priority=false",
                    json=event,
                    timeout=10
                )
                if response.status_code == 201:
                    created_events.append(response.json())
            
            # Test conflict detection
            response = requests.get(
                f"{self.api_base_url}/api/v1/events/priority/conflicts?cognito_sub={self.demo_user_id}&min_priority_diff=2",
                timeout=10
            )
            
            if response.status_code == 200:
                conflict_analysis = response.json()
                conflicts_detected = conflict_analysis.get('conflicts_detected', 0)
                
                if conflicts_detected > 0:
                    conflicts = conflict_analysis.get('conflicts', [])
                    high_priority_conflicts = [c for c in conflicts if c.get('priority_difference', 0) >= 2]
                    
                    return "PASS", f"Conflict detection successful: {conflicts_detected} conflicts found, {len(high_priority_conflicts)} with significant priority differences", {
                        "conflicts_detected": conflicts_detected,
                        "high_priority_conflicts": len(high_priority_conflicts),
                        "sample_conflict": conflicts[0] if conflicts else None,
                        "events_created": len(created_events)
                    }
                else:
                    return "WARNING", "No conflicts detected despite overlapping events", {
                        "conflicts_detected": conflicts_detected,
                        "events_created": len(created_events)
                    }
            else:
                return "FAIL", f"Conflict detection failed with status {response.status_code}", {"response": response.text}
                
        except Exception as e:
            return "FAIL", f"Conflict detection test failed: {str(e)}", {"error": str(e)}
    
    # Test 4: Analytics Integration
    
    def test_priority_analytics_endpoints(self) -> Tuple[str, str, Dict]:
        """Test priority analytics endpoints"""
        try:
            # Test priority trends
            trends_response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/priority/trends?cognito_sub={self.demo_user_id}&days_back=7",
                timeout=10
            )
            
            # Test BERT performance metrics
            bert_response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/bert/performance?cognito_sub={self.demo_user_id}&days_back=7",
                timeout=10
            )
            
            # Test conflict resolution effectiveness
            conflict_response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/conflicts/resolution-effectiveness?cognito_sub={self.demo_user_id}&days_back=7",
                timeout=10
            )
            
            results = {
                "priority_trends": trends_response.status_code == 200,
                "bert_performance": bert_response.status_code == 200,
                "conflict_effectiveness": conflict_response.status_code == 200
            }
            
            successful_endpoints = sum(results.values())
            total_endpoints = len(results)
            
            if successful_endpoints == total_endpoints:
                # Extract some sample data
                sample_data = {}
                if results["priority_trends"]:
                    trends_data = trends_response.json()
                    sample_data["trends"] = {
                        "total_events": trends_data.get("insights", {}).get("total_events_analyzed", 0),
                        "trend_direction": trends_data.get("insights", {}).get("trend_direction", "unknown")
                    }
                
                if results["bert_performance"]:
                    bert_data = bert_response.json()
                    sample_data["bert"] = {
                        "bert_adoption_rate": bert_data.get("classification_overview", {}).get("bert_adoption_rate", 0),
                        "total_events": bert_data.get("classification_overview", {}).get("total_events", 0)
                    }
                
                return "PASS", f"All {total_endpoints} analytics endpoints operational", {
                    "endpoints_tested": results,
                    "sample_data": sample_data
                }
            elif successful_endpoints > 0:
                return "WARNING", f"{successful_endpoints}/{total_endpoints} analytics endpoints working", {"endpoints_tested": results}
            else:
                return "FAIL", f"All {total_endpoints} analytics endpoints failed", {"endpoints_tested": results}
                
        except Exception as e:
            return "FAIL", f"Analytics endpoints test failed: {str(e)}", {"error": str(e)}
    
    # Test 5: Performance Testing
    
    def test_classification_performance(self) -> Tuple[str, str, Dict]:
        """Test BERT classification performance under load"""
        try:
            test_events = [
                {
                    "title": f"Test Event {i}",
                    "description": f"Performance test event number {i} with sample description for classification testing",
                    "location": "Test Location"
                }
                for i in range(20)  # Test with 20 events
            ]
            
            start_time = time.time()
            response_times = []
            successful_classifications = 0
            
            for event in test_events:
                event_start = time.time()
                
                try:
                    response = requests.post(
                        f"{self.api_base_url}/api/v1/nlp/classify-priority",
                        json=event,
                        timeout=5
                    )
                    
                    event_time = time.time() - event_start
                    response_times.append(event_time)
                    
                    if response.status_code == 200:
                        successful_classifications += 1
                        
                except Exception:
                    response_times.append(5.0)  # Timeout
            
            total_time = time.time() - start_time
            avg_response_time = statistics.mean(response_times) if response_times else 0
            success_rate = successful_classifications / len(test_events) * 100
            
            if success_rate >= 90 and avg_response_time < 1.0:
                return "PASS", f"Performance test passed: {success_rate:.1f}% success rate, {avg_response_time:.3f}s avg response time", {
                    "total_requests": len(test_events),
                    "successful_requests": successful_classifications,
                    "success_rate": success_rate,
                    "total_time": total_time,
                    "average_response_time": avg_response_time,
                    "max_response_time": max(response_times) if response_times else 0
                }
            elif success_rate >= 80:
                return "WARNING", f"Performance acceptable but could be improved: {success_rate:.1f}% success rate, {avg_response_time:.3f}s avg response time", {
                    "total_requests": len(test_events),
                    "successful_requests": successful_classifications,
                    "success_rate": success_rate,
                    "average_response_time": avg_response_time
                }
            else:
                return "FAIL", f"Performance test failed: {success_rate:.1f}% success rate, {avg_response_time:.3f}s avg response time", {
                    "total_requests": len(test_events),
                    "successful_requests": successful_classifications,
                    "success_rate": success_rate,
                    "average_response_time": avg_response_time
                }
                
        except Exception as e:
            return "FAIL", f"Performance test failed: {str(e)}", {"error": str(e)}
    
    def test_concurrent_access(self) -> Tuple[str, str, Dict]:
        """Test system under concurrent access"""
        try:
            def create_event_worker(worker_id):
                """Worker function for concurrent event creation"""
                event = {
                    "title": f"Concurrent Test Event {worker_id}",
                    "description": f"Event created by worker {worker_id} for concurrency testing",
                    "start_time": (datetime.now() + timedelta(hours=6+worker_id)).isoformat(),
                    "end_time": (datetime.now() + timedelta(hours=7+worker_id)).isoformat(),
                    "location": f"Test Room {worker_id}"
                }
                
                try:
                    response = requests.post(
                        f"{self.api_base_url}/api/v1/events?cognito_sub={self.demo_user_id}&auto_classify_priority=true",
                        json=event,
                        timeout=10
                    )
                    return response.status_code == 201
                except Exception:
                    return False
            
            # Test with 10 concurrent workers
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                start_time = time.time()
                futures = [executor.submit(create_event_worker, i) for i in range(10)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
                total_time = time.time() - start_time
            
            successful_requests = sum(results)
            total_requests = len(results)
            success_rate = successful_requests / total_requests * 100
            
            if success_rate >= 90:
                return "PASS", f"Concurrency test passed: {successful_requests}/{total_requests} requests successful in {total_time:.3f}s", {
                    "successful_requests": successful_requests,
                    "total_requests": total_requests,
                    "success_rate": success_rate,
                    "total_time": total_time,
                    "avg_time_per_request": total_time / total_requests
                }
            elif success_rate >= 70:
                return "WARNING", f"Concurrency test partially successful: {successful_requests}/{total_requests} requests successful", {
                    "successful_requests": successful_requests,
                    "total_requests": total_requests,
                    "success_rate": success_rate
                }
            else:
                return "FAIL", f"Concurrency test failed: only {successful_requests}/{total_requests} requests successful", {
                    "successful_requests": successful_requests,
                    "total_requests": total_requests,
                    "success_rate": success_rate
                }
                
        except Exception as e:
            return "FAIL", f"Concurrency test failed: {str(e)}", {"error": str(e)}
    
    # Test 6: Data Validation
    
    def test_demo_data_compatibility(self) -> Tuple[str, str, Dict]:
        """Test that demo data can be generated and processed"""
        try:
            # Check if demo data script exists and can be imported
            demo_script = Path("create_demo_data.py")
            if not demo_script.exists():
                return "FAIL", "Demo data script not found", {"script_path": str(demo_script)}
            
            # Try to import and test the demo data generator
            import importlib.util
            spec = importlib.util.spec_from_file_location("create_demo_data", demo_script)
            demo_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(demo_module)
            
            if hasattr(demo_module, 'DemoDataGenerator'):
                generator = demo_module.DemoDataGenerator()
                
                # Generate a small sample of demo events
                sample_events = generator.generate_user_events(user_id=999, num_events=5)
                
                if len(sample_events) == 5:
                    priority_distribution = {}
                    for event in sample_events:
                        priority = event.expected_priority
                        priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
                    
                    return "PASS", f"Demo data generation successful: {len(sample_events)} events created", {
                        "events_generated": len(sample_events),
                        "priority_distribution": priority_distribution,
                        "sample_event": {
                            "title": sample_events[0].title,
                            "priority": sample_events[0].expected_priority,
                            "type": sample_events[0].event_type
                        }
                    }
                else:
                    return "FAIL", f"Demo data generation failed: expected 5 events, got {len(sample_events)}", {}
            else:
                return "FAIL", "DemoDataGenerator class not found in demo script", {}
                
        except Exception as e:
            return "FAIL", f"Demo data compatibility test failed: {str(e)}", {"error": str(e)}
    
    # Main Test Execution Methods
    
    def run_core_integration_tests(self):
        """Run core system integration tests"""
        print("\n🔗 CORE INTEGRATION TESTS")
        print("=" * 70)
        
        self.run_test("Event Creation with BERT Priority", self.test_event_creation_with_bert_priority)
        self.run_test("Priority-Based Event Filtering", self.test_priority_based_event_filtering)
        self.run_test("BERT NLP Endpoint", self.test_bert_nlp_endpoint)
        self.run_test("Model Status Endpoint", self.test_model_status_endpoint)
        self.run_test("Priority Conflict Detection", self.test_priority_conflict_detection)
        self.run_test("Analytics Endpoints", self.test_priority_analytics_endpoints)
    
    def run_performance_tests(self):
        """Run performance and load tests"""
        print("\n⚡ PERFORMANCE TESTS")
        print("=" * 70)
        
        self.run_test("Classification Performance", self.test_classification_performance)
        self.run_test("Concurrent Access", self.test_concurrent_access)
    
    def run_data_validation_tests(self):
        """Run data validation tests"""
        print("\n📊 DATA VALIDATION TESTS")
        print("=" * 70)
        
        self.run_test("Demo Data Compatibility", self.test_demo_data_compatibility)
    
    def cleanup_test_data(self):
        """Clean up test data created during testing"""
        try:
            # Get all events for test user
            response = requests.get(
                f"{self.api_base_url}/api/v1/events?cognito_sub={self.demo_user_id}&limit=1000",
                timeout=10
            )
            
            if response.status_code == 200:
                events = response.json()
                deleted_count = 0
                
                for event in events:
                    if event.get('title', '').startswith(('Test', 'Emergency', 'Critical', 'Concurrent', 'Casual')):
                        delete_response = requests.delete(
                            f"{self.api_base_url}/api/v1/events/{event['id']}?cognito_sub={self.demo_user_id}",
                            timeout=10
                        )
                        if delete_response.status_code == 200:
                            deleted_count += 1
                
                print(f"\n🧹 Cleanup: Deleted {deleted_count} test events")
                
        except Exception as e:
            print(f"\n⚠️  Cleanup warning: {str(e)}")
    
    def generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final integration test report"""
        total_time = time.time() - self.start_time
        
        # Categorize results
        status_counts = {"PASS": 0, "FAIL": 0, "WARNING": 0}
        test_categories = {
            "core_integration": [],
            "performance": [],
            "data_validation": []
        }
        
        for result in self.results:
            status_counts[result.status] += 1
            
            # Categorize tests
            if any(keyword in result.test_name.lower() for keyword in ['event', 'bert', 'nlp', 'conflict', 'analytics']):
                test_categories["core_integration"].append(result)
            elif any(keyword in result.test_name.lower() for keyword in ['performance', 'concurrent']):
                test_categories["performance"].append(result)
            else:
                test_categories["data_validation"].append(result)
        
        # Calculate scores
        total_tests = len(self.results)
        if total_tests > 0:
            pass_rate = status_counts["PASS"] / total_tests * 100
            fail_rate = status_counts["FAIL"] / total_tests * 100
            warning_rate = status_counts["WARNING"] / total_tests * 100
        else:
            pass_rate = fail_rate = warning_rate = 0
        
        # Determine integration readiness
        if pass_rate >= 90 and fail_rate == 0:
            integration_status = "FULLY INTEGRATED"
        elif pass_rate >= 80 and fail_rate <= 10:
            integration_status = "MOSTLY INTEGRATED"
        elif pass_rate >= 60:
            integration_status = "PARTIALLY INTEGRATED"
        else:
            integration_status = "INTEGRATION ISSUES"
        
        # Performance analysis
        performance_results = test_categories["performance"]
        avg_response_time = 0
        if performance_results:
            response_times = []
            for result in performance_results:
                if result.details and "average_response_time" in result.details:
                    response_times.append(result.details["average_response_time"])
            avg_response_time = statistics.mean(response_times) if response_times else 0
        
        return {
            "integration_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_execution_time": round(total_time, 2),
                "integration_status": integration_status,
                "total_tests": total_tests,
                "pass_rate": round(pass_rate, 1),
                "fail_rate": round(fail_rate, 1),
                "warning_rate": round(warning_rate, 1),
                "status_breakdown": status_counts
            },
            "category_breakdown": {
                category: {
                    "total": len(results),
                    "passed": len([r for r in results if r.status == "PASS"]),
                    "failed": len([r for r in results if r.status == "FAIL"]),
                    "warnings": len([r for r in results if r.status == "WARNING"])
                }
                for category, results in test_categories.items()
            },
            "performance_metrics": {
                "average_response_time": round(avg_response_time, 3),
                "performance_status": "GOOD" if avg_response_time < 0.5 else "ACCEPTABLE" if avg_response_time < 1.0 else "NEEDS_IMPROVEMENT"
            },
            "failed_tests": [
                {
                    "test_name": r.test_name,
                    "message": r.message,
                    "error": r.error
                }
                for r in self.results if r.status == "FAIL"
            ],
            "warnings": [
                {
                    "test_name": r.test_name,
                    "message": r.message
                }
                for r in self.results if r.status == "WARNING"
            ],
            "integration_recommendations": self._generate_integration_recommendations()
        }
    
    def _generate_integration_recommendations(self) -> List[str]:
        """Generate integration recommendations based on test results"""
        recommendations = []
        
        fail_count = len([r for r in self.results if r.status == "FAIL"])
        warning_count = len([r for r in self.results if r.status == "WARNING"])
        
        # BERT-specific recommendations
        bert_tests = [r for r in self.results if 'bert' in r.test_name.lower() or 'nlp' in r.test_name.lower()]
        bert_failures = [r for r in bert_tests if r.status == "FAIL"]
        
        if bert_failures:
            recommendations.append("🤖 BERT integration has issues - check model loading and training")
        
        # Performance recommendations
        performance_tests = [r for r in self.results if 'performance' in r.test_name.lower() or 'concurrent' in r.test_name.lower()]
        performance_failures = [r for r in performance_tests if r.status in ["FAIL", "WARNING"]]
        
        if performance_failures:
            recommendations.append("⚡ Performance optimization needed - consider caching and load balancing")
        
        # General recommendations
        if fail_count > 3:
            recommendations.append("🔧 Multiple integration failures detected - systematic review required")
        
        if warning_count > 2:
            recommendations.append("⚠️ Address warnings to ensure optimal production performance")
        
        if fail_count == 0 and warning_count <= 1:
            recommendations.append("✅ System integration is excellent - ready for production deployment")
        
        return recommendations

async def main():
    """Main integration testing function"""
    parser = argparse.ArgumentParser(description="Final Integration Testing for KairoCal BERT System")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--full-test", action="store_true", help="Run all integration tests")
    parser.add_argument("--performance-test", action="store_true", help="Run performance tests only")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--output", help="Save report to JSON file")
    parser.add_argument("--cleanup", action="store_true", help="Clean up test data after testing")
    
    args = parser.parse_args()
    
    print("🚀 KairoCal BERT Priority Classification System - Final Integration Testing")
    print("=" * 80)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API URL: {args.api_url}")
    print()
    
    # Check if API server is running
    try:
        response = requests.get(f"{args.api_url}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server is not responding properly. Please start the server first.")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Please start the server first.")
        print(f"   Expected API URL: {args.api_url}")
        print("   Start with: uvicorn app.main:app --reload")
        sys.exit(1)
    
    print("✅ API server is running and responding")
    print()
    
    tester = FinalIntegrationTester(api_base_url=args.api_url, verbose=args.verbose)
    
    # Run tests based on arguments
    if args.performance_test:
        tester.run_performance_tests()
    elif args.full_test:
        tester.run_core_integration_tests()
        tester.run_performance_tests()
        tester.run_data_validation_tests()
    else:
        # Default: run core integration tests
        tester.run_core_integration_tests()
        tester.run_data_validation_tests()
    
    # Clean up test data if requested
    if args.cleanup:
        tester.cleanup_test_data()
    
    # Generate and display final report
    report = tester.generate_final_report()
    
    print("\n📊 FINAL INTEGRATION TEST SUMMARY")
    print("=" * 70)
    print(f"🎯 Integration Status: {report['integration_summary']['integration_status']}")
    print(f"📈 Pass Rate: {report['integration_summary']['pass_rate']}%")
    print(f"⏱️  Total Time: {report['integration_summary']['total_execution_time']}s")
    print(f"📋 Total Tests: {report['integration_summary']['total_tests']}")
    
    status_breakdown = report['integration_summary']['status_breakdown']
    print(f"✅ Passed: {status_breakdown['PASS']}")
    print(f"❌ Failed: {status_breakdown['FAIL']}")
    print(f"⚠️  Warnings: {status_breakdown['WARNING']}")
    
    # Performance summary
    if 'performance_metrics' in report:
        perf = report['performance_metrics']
        print(f"⚡ Avg Response Time: {perf['average_response_time']}s ({perf['performance_status']})")
    
    # Show failures and warnings
    if report['failed_tests']:
        print("\n❌ FAILED TESTS:")
        for test in report['failed_tests']:
            print(f"  • {test['test_name']}: {test['message']}")
    
    if report['warnings']:
        print("\n⚠️  WARNINGS:")
        for warning in report['warnings']:
            print(f"  • {warning['test_name']}: {warning['message']}")
    
    # Show recommendations
    if report['integration_recommendations']:
        print("\n💡 INTEGRATION RECOMMENDATIONS:")
        for rec in report['integration_recommendations']:
            print(f"  • {rec}")
    
    # Save report if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n💾 Full integration report saved to: {args.output}")
    
    # Final status message
    integration_status = report['integration_summary']['integration_status']
    if integration_status == "FULLY INTEGRATED":
        print(f"\n🎉 BERT Priority Classification System is fully integrated and ready for production!")
        sys.exit(0)
    elif integration_status == "MOSTLY INTEGRATED":
        print(f"\n✅ System is mostly integrated with minor issues to address.")
        sys.exit(0)
    else:
        print(f"\n🛠️  Integration issues detected. Please address failed tests before production deployment.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
