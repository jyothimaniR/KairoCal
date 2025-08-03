# backend/validate_bert_training.py
"""
BERT Training Validation Script
Validates trained model performance and tests classification accuracy
"""

import sys
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import numpy as np

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.nlp.model_loader import load_bert_model, get_model_status, is_trained_model_available
from app.nlp.bert_training_data_generator import BERTTrainingDataGenerator
from app.config import get_settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BERTValidationTester:
    """Comprehensive BERT model validation and testing"""
    
    def __init__(self):
        self.settings = get_settings()
        self.priority_labels = {
            1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"
        }
        
    def load_model_info(self) -> Dict[str, Any]:
        """Load and display model information"""
        logger.info("📊 Loading model information...")
        
        model_info = get_model_status()
        
        if not model_info['loaded']:
            logger.error("❌ No model loaded")
            return model_info
            
        logger.info("✅ Model Status:")
        logger.info(f"   Loaded: {model_info['loaded']}")
        logger.info(f"   Trained: {model_info['trained']}")
        logger.info(f"   Device: {model_info['device']}")
        logger.info(f"   Model Path: {model_info['model_path']}")
        
        if 'metadata' in model_info and model_info['metadata']:
            metadata = model_info['metadata']
            logger.info("📈 Training Metadata:")
            logger.info(f"   Training Date: {metadata.get('training_date', 'Unknown')}")
            logger.info(f"   Accuracy: {metadata.get('accuracy', 'Unknown')}")
            logger.info(f"   Training Duration: {metadata.get('training_duration', 'Unknown')} minutes")
            
        return model_info
        
    def test_sample_events(self) -> Dict[str, Any]:
        """Test model on comprehensive sample events"""
        logger.info("🧪 Testing model on sample events...")
        
        try:
            classifier = load_bert_model()
        except Exception as e:
            logger.error(f"❌ Failed to load model: {str(e)}")
            return {"error": str(e)}
            
        # Comprehensive test cases covering all priority levels
        test_events = [
            # Priority 5 (Critical)
            {
                "title": "URGENT: CEO Emergency Meeting",
                "description": "Critical business decision required immediately due to market crisis",
                "location": "Executive Boardroom",
                "expected_priority": 5,
                "category": "Critical"
            },
            {
                "title": "CRITICAL: System Outage Response",
                "description": "Production servers down, immediate action required",
                "location": "IT Operations Center", 
                "expected_priority": 5,
                "category": "Critical"
            },
            {
                "title": "ASAP: Legal Emergency",
                "description": "Urgent legal matter requiring immediate attorney consultation",
                "location": "Legal Department",
                "expected_priority": 5,
                "category": "Critical"
            },
            
            # Priority 4 (High)
            {
                "title": "Important: Client Presentation",
                "description": "Quarterly review presentation for our largest client",
                "location": "Conference Room A",
                "expected_priority": 4,
                "category": "High"
            },
            {
                "title": "Executive Interview", 
                "description": "Final round interview for VP position",
                "location": "Executive Office",
                "expected_priority": 4,
                "category": "High"
            },
            {
                "title": "Important: Budget Approval Meeting",
                "description": "Annual budget review and approval session",
                "location": "Finance Department",
                "expected_priority": 4,
                "category": "High"
            },
            
            # Priority 3 (Medium)
            {
                "title": "Weekly Team Meeting",
                "description": "Regular team sync and project updates",
                "location": "Conference Room B",
                "expected_priority": 3,
                "category": "Medium"
            },
            {
                "title": "Project Planning Session",
                "description": "Planning meeting for Q4 project roadmap", 
                "location": "Meeting Room 1",
                "expected_priority": 3,
                "category": "Medium"
            },
            {
                "title": "Department Standup",
                "description": "Daily standup meeting for development team",
                "location": "Open Office Area",
                "expected_priority": 3,
                "category": "Medium"
            },
            
            # Priority 2 (Low)
            {
                "title": "Optional Training Workshop",
                "description": "Professional development workshop on new technologies",
                "location": "Training Room",
                "expected_priority": 2,
                "category": "Low"
            },
            {
                "title": "Team Lunch",
                "description": "Casual team lunch and social gathering",
                "location": "Restaurant",
                "expected_priority": 2,
                "category": "Low"
            },
            {
                "title": "Networking Event",
                "description": "Industry networking and knowledge sharing event",
                "location": "Conference Center",
                "expected_priority": 2,
                "category": "Low"
            },
            
            # Priority 1 (Very Low)
            {
                "title": "Coffee with colleague",
                "description": "Informal coffee chat with team member",
                "location": "Coffee Shop",
                "expected_priority": 1,
                "category": "Very Low"
            },
            {
                "title": "Personal appointment",
                "description": "Personal errands and appointments",
                "location": "Various",
                "expected_priority": 1,
                "category": "Very Low"
            },
            {
                "title": "Social Event",
                "description": "Optional company social gathering",
                "location": "Office Lounge",
                "expected_priority": 1,
                "category": "Very Low"
            }
        ]
        
        results = []
        correct_predictions = 0
        total_predictions = len(test_events)
        
        logger.info(f"🎯 Testing {total_predictions} sample events:")
        logger.info("-" * 80)
        
        for i, event in enumerate(test_events, 1):
            try:
                # Get prediction
                priority, confidence = classifier.predict(event)
                
                # Check if prediction is correct
                is_correct = priority == event["expected_priority"]
                if is_correct:
                    correct_predictions += 1
                
                # Calculate priority difference (for partial credit)
                priority_diff = abs(priority - event["expected_priority"])
                
                result = {
                    "event_title": event["title"],
                    "category": event["category"],
                    "predicted_priority": priority,
                    "expected_priority": event["expected_priority"],
                    "confidence": confidence,
                    "correct": is_correct,
                    "priority_difference": priority_diff,
                    "model_used": "BERT" if classifier.is_trained else "Fallback"
                }
                results.append(result)
                
                # Status indicator
                status = "✅" if is_correct else "❌" if priority_diff > 1 else "⚠️"
                
                logger.info(f"{i:2d}. {status} {event['category']:>10} | '{event['title'][:35]:<35}' → "
                          f"P{priority} (Expected: P{event['expected_priority']}) | "
                          f"Conf: {confidence:.3f}")
                
            except Exception as e:
                logger.error(f"❌ Error processing event {i}: {str(e)}")
                result = {
                    "event_title": event["title"],
                    "error": str(e),
                    "correct": False
                }
                results.append(result)
        
        # Calculate accuracy metrics
        accuracy = correct_predictions / total_predictions
        
        # Calculate accuracy within 1 priority level (partial credit)
        close_predictions = sum(1 for r in results if r.get("priority_difference", 10) <= 1)
        close_accuracy = close_predictions / total_predictions
        
        # Calculate average confidence
        confidences = [r["confidence"] for r in results if "confidence" in r]
        avg_confidence = np.mean(confidences) if confidences else 0.0
        
        logger.info("-" * 80)
        logger.info("📊 Validation Results:")
        logger.info(f"   Exact Accuracy: {accuracy:.2%} ({correct_predictions}/{total_predictions})")
        logger.info(f"   Close Accuracy (±1): {close_accuracy:.2%} ({close_predictions}/{total_predictions})")
        logger.info(f"   Average Confidence: {avg_confidence:.3f}")
        logger.info(f"   Model Type: {'BERT' if classifier.is_trained else 'Fallback/Rule-based'}")
        
        return {
            "total_events": total_predictions,
            "correct_predictions": correct_predictions,
            "exact_accuracy": accuracy,
            "close_accuracy": close_accuracy,
            "average_confidence": avg_confidence,
            "results": results,
            "model_trained": classifier.is_trained
        }
        
    def test_priority_distribution(self) -> Dict[str, Any]:
        """Test model performance across different priority levels"""
        logger.info("📈 Testing priority distribution performance...")
        
        try:
            classifier = load_bert_model()
            data_generator = BERTTrainingDataGenerator()
            
            # Generate test data for each priority level
            test_size_per_priority = 20
            distribution_results = {}
            
            for priority in range(1, 6):
                logger.info(f"   Testing Priority {priority} ({self.priority_labels[priority]})...")
                
                # Generate test examples for this priority
                examples = []
                for _ in range(test_size_per_priority):
                    example = data_generator.generate_training_example(priority)
                    examples.append(example)
                
                # Test predictions
                correct = 0
                confidences = []
                
                for example in examples:
                    pred_priority, confidence = classifier.predict(example)
                    confidences.append(confidence)
                    
                    if pred_priority == priority:
                        correct += 1
                
                accuracy = correct / test_size_per_priority
                avg_confidence = np.mean(confidences)
                
                distribution_results[priority] = {
                    "priority_label": self.priority_labels[priority],
                    "accuracy": accuracy,
                    "average_confidence": avg_confidence,
                    "correct_predictions": correct,
                    "total_predictions": test_size_per_priority
                }
                
                logger.info(f"      Accuracy: {accuracy:.2%}, Avg Confidence: {avg_confidence:.3f}")
            
            return distribution_results
            
        except Exception as e:
            logger.error(f"❌ Priority distribution test failed: {str(e)}")
            return {"error": str(e)}
            
    def test_edge_cases(self) -> Dict[str, Any]:
        """Test model on edge cases and challenging scenarios"""
        logger.info("🔍 Testing edge cases and challenging scenarios...")
        
        try:
            classifier = load_bert_model()
        except Exception as e:
            logger.error(f"❌ Failed to load model: {str(e)}")
            return {"error": str(e)}
            
        edge_cases = [
            # Empty/minimal input
            {
                "title": "Meeting",
                "description": "",
                "case": "Minimal input"
            },
            
            # Mixed priority signals
            {
                "title": "Urgent coffee break",
                "description": "Important casual meeting",
                "case": "Conflicting signals"
            },
            
            # Long description
            {
                "title": "Strategy Meeting",
                "description": "This is a very long description that contains multiple sentences and various pieces of information about the meeting including objectives, attendees, agenda items, and expected outcomes for the quarterly business review session.",
                "case": "Long description"
            },
            
            # Special characters
            {
                "title": "CEO Meeting @ 2PM!!!",
                "description": "URGENT: Review Q3 financials & discuss strategic initiatives",
                "case": "Special characters"
            },
            
            # Time-related keywords
            {
                "title": "Deadline Review",
                "description": "Final review before tomorrow's deadline",
                "case": "Time pressure"
            }
        ]
        
        edge_results = []
        
        for case in edge_cases:
            try:
                priority, confidence = classifier.predict(case)
                
                result = {
                    "case": case["case"],
                    "title": case["title"],
                    "priority": priority,
                    "priority_label": self.priority_labels[priority],
                    "confidence": confidence,
                    "success": True
                }
                
                logger.info(f"   {case['case']:>18}: P{priority} ({self.priority_labels[priority]}) | Conf: {confidence:.3f}")
                
            except Exception as e:
                result = {
                    "case": case["case"],
                    "error": str(e),
                    "success": False
                }
                logger.error(f"   {case['case']:>18}: ERROR - {str(e)}")
                
            edge_results.append(result)
            
        return {"edge_case_results": edge_results}
        
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run complete validation suite"""
        logger.info("🚀 Starting Comprehensive BERT Model Validation")
        logger.info("=" * 80)
        
        validation_start = datetime.now()
        
        # Check if trained model is available
        if not is_trained_model_available():
            logger.warning("⚠️ No trained model found. Please run training first.")
            logger.info("💡 Run: python train_bert_model.py")
            return {"error": "No trained model available"}
        
        results = {}
        
        try:
            # 1. Load model information
            results["model_info"] = self.load_model_info()
            
            # 2. Test sample events
            results["sample_tests"] = self.test_sample_events()
            
            # 3. Test priority distribution
            results["distribution_tests"] = self.test_priority_distribution()
            
            # 4. Test edge cases
            results["edge_case_tests"] = self.test_edge_cases()
            
            # Summary
            validation_duration = (datetime.now() - validation_start).total_seconds()
            
            logger.info("=" * 80)
            logger.info("🎉 VALIDATION COMPLETED!")
            logger.info(f"⏱️ Duration: {validation_duration:.2f} seconds")
            
            if "sample_tests" in results and "exact_accuracy" in results["sample_tests"]:
                accuracy = results["sample_tests"]["exact_accuracy"]
                logger.info(f"🎯 Overall Accuracy: {accuracy:.2%}")
                
                if accuracy >= 0.8:
                    logger.info("✅ Model performance is EXCELLENT!")
                elif accuracy >= 0.6:
                    logger.info("⚠️ Model performance is GOOD but could be improved")
                else:
                    logger.info("❌ Model performance needs improvement - consider retraining")
            
            logger.info("=" * 80)
            
            results["validation_summary"] = {
                "duration_seconds": validation_duration,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Validation failed: {str(e)}")
            return {"error": str(e)}

def main():
    """Main validation script entry point"""
    print("🤖 KairoCal BERT Model Validation")
    print("=" * 60)
    
    validator = BERTValidationTester()
    results = validator.run_comprehensive_validation()
    
    # Save results to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"validation_results_{timestamp}.json"
    
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Validation results saved to: {results_file}")
    except Exception as e:
        print(f"⚠️ Failed to save results: {str(e)}")
    
    # Exit with appropriate code
    if "error" in results:
        print(f"\n❌ Validation failed: {results['error']}")
        sys.exit(1)
    else:
        print("\n✅ Validation completed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
