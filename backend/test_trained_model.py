#!/usr/bin/env python3
"""
Post-Training Model Validation for KairoCal BERT Priority Classifier
Tests the newly trained model against sample events and compares with fallback system
"""

import sys
import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrainedModelValidator:
    """Comprehensive validation of the trained BERT model"""
    
    def __init__(self):
        self.model_path = "models/bert_priority_classifier"
        self.test_events = self._create_test_events()
        self.results = []
        
    def _create_test_events(self) -> List[Dict[str, Any]]:
        """Create comprehensive test events with expected priorities"""
        return [
            {
                "title": "URGENT: Server crashed, need immediate fix",
                "description": "Production server down, customers can't access the application. Need immediate attention from DevOps team.",
                "start_time": (datetime.now() + timedelta(minutes=5)).isoformat(),
                "location": "Data Center",
                "expected_priority": 5,  # Critical
                "expected_range": [4, 5],
                "category": "emergency"
            },
            {
                "title": "Team lunch next Friday",
                "description": "Casual team lunch at the local restaurant. Optional attendance.",
                "start_time": (datetime.now() + timedelta(days=7)).isoformat(),
                "location": "Restaurant",
                "expected_priority": 1,  # Very Low
                "expected_range": [1, 2],
                "category": "social"
            },
            {
                "title": "Board meeting with CEO tomorrow",
                "description": "Quarterly board meeting to discuss company performance and strategic direction. Mandatory attendance for all directors.",
                "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
                "location": "Conference Room A",
                "expected_priority": 5,  # Critical
                "expected_range": [4, 5],
                "category": "business_critical"
            },
            {
                "title": "Doctor appointment next week",
                "description": "Annual health checkup with family physician. Routine appointment.",
                "start_time": (datetime.now() + timedelta(days=8)).isoformat(),
                "location": "Medical Center",
                "expected_priority": 3,  # Medium
                "expected_range": [2, 3],
                "category": "personal_health"
            },
            {
                "title": "Coffee break in 10 minutes",
                "description": "Quick coffee break with colleagues. Very informal.",
                "start_time": (datetime.now() + timedelta(minutes=10)).isoformat(),
                "location": "Kitchen",
                "expected_priority": 1,  # Very Low
                "expected_range": [1, 2],
                "category": "break"
            },
            {
                "title": "Client presentation deadline tomorrow",
                "description": "Final presentation for major client proposal. Multiple stakeholders involved. High visibility project.",
                "start_time": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
                "location": "Client Office",
                "expected_priority": 4,  # High
                "expected_range": [4, 5],
                "category": "client_work"
            },
            {
                "title": "Optional training workshop",
                "description": "Professional development workshop on new technologies. Nice to have but not required.",
                "start_time": (datetime.now() + timedelta(days=5)).isoformat(),
                "location": "Training Room",
                "expected_priority": 2,  # Low
                "expected_range": [1, 3],
                "category": "training"
            },
            {
                "title": "Weekly team standup",
                "description": "Regular weekly team standup meeting to discuss progress and blockers.",
                "start_time": (datetime.now() + timedelta(days=2)).isoformat(),
                "location": "Conference Room B",
                "expected_priority": 3,  # Medium
                "expected_range": [2, 4],
                "category": "regular_meeting"
            }
        ]
    
    def load_trained_model(self):
        """Load the trained BERT model"""
        try:
            from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
            
            # Check if model files exist
            model_path = Path(self.model_path)
            if not model_path.exists():
                logger.error(f"❌ Model directory not found: {model_path}")
                return None
                
            model_files = list(model_path.glob("*.bin")) + list(model_path.glob("*.json"))
            if not model_files:
                logger.error(f"❌ No model files found in: {model_path}")
                return None
            
            logger.info(f"📂 Loading trained model from: {model_path}")
            logger.info(f"📁 Found model files: {[f.name for f in model_files]}")
            
            # Initialize classifier (will load trained model automatically)
            classifier = AdvancedEventPriorityClassifier(model_path=str(model_path))
            
            if classifier.is_trained:
                logger.info("✅ Successfully loaded trained BERT model")
                return classifier
            else:
                logger.warning("⚠️ Model loaded but not marked as trained")
                return classifier
                
        except ImportError as e:
            logger.error(f"❌ Failed to import BERT classifier: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Failed to load trained model: {e}")
            return None
    
    def load_fallback_system(self):
        """Load the rule-based fallback system for comparison"""
        try:
            from app.nlp.priority_inference import PriorityInferenceEngine
            
            logger.info("📂 Loading rule-based fallback system")
            fallback = PriorityInferenceEngine()
            logger.info("✅ Successfully loaded fallback system")
            return fallback
            
        except ImportError as e:
            logger.error(f"❌ Failed to import fallback system: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Failed to load fallback system: {e}")
            return None
    
    def test_model_predictions(self, bert_classifier, fallback_system):
        """Test both models on sample events"""
        logger.info("🧪 Testing model predictions on sample events")
        logger.info("=" * 80)
        
        bert_correct = 0
        fallback_correct = 0
        
        for i, event in enumerate(self.test_events, 1):
            logger.info(f"\n📝 Test Event {i}: {event['category'].upper()}")
            logger.info(f"   Title: '{event['title']}'")
            logger.info(f"   Expected Priority: {event['expected_priority']} (range: {event['expected_range']})")
            
            # Test BERT model
            bert_priority = None
            bert_confidence = 0.0
            bert_status = "❌ FAILED"
            
            if bert_classifier:
                try:
                    bert_priority, bert_confidence = bert_classifier.predict(event)
                    bert_correct_prediction = bert_priority in event['expected_range']
                    if bert_correct_prediction:
                        bert_correct += 1
                        bert_status = "✅ CORRECT"
                    else:
                        bert_status = "❌ INCORRECT"
                        
                    logger.info(f"   🤖 BERT Prediction: Priority {bert_priority} ({bert_classifier.priority_labels[bert_priority]}) - Confidence: {bert_confidence:.3f} {bert_status}")
                    
                except Exception as e:
                    logger.error(f"   🤖 BERT Prediction: FAILED - {str(e)}")
            else:
                logger.error(f"   🤖 BERT Prediction: MODEL NOT AVAILABLE")
            
            # Test fallback system
            fallback_priority = None
            fallback_confidence = 0.0
            fallback_status = "❌ FAILED"
            
            if fallback_system:
                try:
                    fallback_priority = fallback_system.infer_priority(
                        event['title'], 
                        event['description']
                    )
                    fallback_confidence = 0.8  # Fallback system doesn't provide confidence
                    fallback_correct_prediction = fallback_priority in event['expected_range']
                    if fallback_correct_prediction:
                        fallback_correct += 1
                        fallback_status = "✅ CORRECT"
                    else:
                        fallback_status = "❌ INCORRECT"
                        
                    logger.info(f"   📋 Rule-based: Priority {fallback_priority} - Confidence: {fallback_confidence:.3f} {fallback_status}")
                    
                except Exception as e:
                    logger.error(f"   📋 Rule-based: FAILED - {str(e)}")
            else:
                logger.error(f"   📋 Rule-based: SYSTEM NOT AVAILABLE")
            
            # Store results
            self.results.append({
                'event': event,
                'bert_prediction': {
                    'priority': bert_priority,
                    'confidence': bert_confidence,
                    'correct': bert_priority in event['expected_range'] if bert_priority else False
                },
                'fallback_prediction': {
                    'priority': fallback_priority,
                    'confidence': fallback_confidence,
                    'correct': fallback_priority in event['expected_range'] if fallback_priority else False
                }
            })
        
        # Summary
        total_events = len(self.test_events)
        bert_accuracy = (bert_correct / total_events) * 100 if total_events > 0 else 0
        fallback_accuracy = (fallback_correct / total_events) * 100 if total_events > 0 else 0
        
        logger.info("\n" + "=" * 80)
        logger.info("📊 PREDICTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"🤖 BERT Model:")
        logger.info(f"   Correct predictions: {bert_correct}/{total_events}")
        logger.info(f"   Accuracy: {bert_accuracy:.1f}%")
        
        logger.info(f"\n📋 Rule-based Fallback:")
        logger.info(f"   Correct predictions: {fallback_correct}/{total_events}")
        logger.info(f"   Accuracy: {fallback_accuracy:.1f}%")
        
        logger.info(f"\n🏆 Performance Comparison:")
        if bert_accuracy > fallback_accuracy:
            improvement = bert_accuracy - fallback_accuracy
            logger.info(f"   ✅ BERT is better by {improvement:.1f} percentage points")
        elif fallback_accuracy > bert_accuracy:
            decline = fallback_accuracy - bert_accuracy
            logger.info(f"   ⚠️ BERT is worse by {decline:.1f} percentage points")
        else:
            logger.info(f"   🤝 Both systems perform equally")
        
        return {
            'bert_accuracy': bert_accuracy,
            'fallback_accuracy': fallback_accuracy,
            'total_events': total_events,
            'bert_correct': bert_correct,
            'fallback_correct': fallback_correct
        }
    
    def analyze_confidence_scores(self):
        """Analyze confidence score distributions"""
        logger.info("\n📈 CONFIDENCE SCORE ANALYSIS")
        logger.info("=" * 50)
        
        bert_confidences = [r['bert_prediction']['confidence'] for r in self.results if r['bert_prediction']['confidence'] > 0]
        fallback_confidences = [r['fallback_prediction']['confidence'] for r in self.results if r['fallback_prediction']['confidence'] > 0]
        
        if bert_confidences:
            bert_avg = sum(bert_confidences) / len(bert_confidences)
            bert_min = min(bert_confidences)
            bert_max = max(bert_confidences)
            logger.info(f"🤖 BERT Confidence Scores:")
            logger.info(f"   Average: {bert_avg:.3f}")
            logger.info(f"   Range: {bert_min:.3f} - {bert_max:.3f}")
            
            # Check if BERT confidences are in expected range (typically lower for new models)
            if bert_avg < 0.5:
                logger.info("   📊 Low confidence typical for newly trained model")
            elif bert_avg > 0.8:
                logger.info("   📊 High confidence indicates good model certainty")
            else:
                logger.info("   📊 Moderate confidence indicates learning progress")
        
        if fallback_confidences:
            fallback_avg = sum(fallback_confidences) / len(fallback_confidences)
            logger.info(f"\n📋 Rule-based Confidence Scores:")
            logger.info(f"   Average: {fallback_avg:.3f}")
            logger.info("   📊 Fixed confidence (rule-based systems don't provide real confidence)")
    
    def check_model_improvement(self):
        """Check for signs of model learning and improvement"""
        logger.info("\n🔍 MODEL IMPROVEMENT ANALYSIS")
        logger.info("=" * 50)
        
        # Check if model files exist and their sizes
        model_path = Path(self.model_path)
        if model_path.exists():
            model_files = list(model_path.glob("*"))
            total_size = sum(f.stat().st_size for f in model_files if f.is_file())
            
            logger.info(f"📂 Model Directory: {model_path}")
            logger.info(f"📁 Number of files: {len(model_files)}")
            logger.info(f"💾 Total size: {total_size / (1024*1024):.1f} MB")
            
            # Check for key files
            key_files = ['pytorch_model.bin', 'config.json', 'training_metadata.json']
            for key_file in key_files:
                file_path = model_path / key_file
                if file_path.exists():
                    size_mb = file_path.stat().st_size / (1024*1024)
                    logger.info(f"   ✅ {key_file}: {size_mb:.1f} MB")
                else:
                    logger.info(f"   ❌ {key_file}: Missing")
            
            # Load training metadata if available
            metadata_file = model_path / 'training_metadata.json'
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    logger.info(f"\n📊 Training Results:")
                    logger.info(f"   Training Date: {metadata.get('training_date', 'Unknown')}")
                    logger.info(f"   Training Duration: {metadata.get('training_duration_minutes', 0):.1f} minutes")
                    
                    if 'training_history' in metadata:
                        history = metadata['training_history']
                        if 'val_accuracy' in history and history['val_accuracy']:
                            final_val_acc = history['val_accuracy'][-1] * 100
                            logger.info(f"   Final Validation Accuracy: {final_val_acc:.1f}%")
                            
                            if final_val_acc > 50:
                                logger.info("   ✅ Good validation accuracy achieved")
                            elif final_val_acc > 30:
                                logger.info("   ⚠️ Moderate validation accuracy")
                            else:
                                logger.info("   ❌ Low validation accuracy")
                    
                except Exception as e:
                    logger.error(f"   ❌ Failed to load training metadata: {e}")
        else:
            logger.error(f"❌ Model directory not found: {model_path}")
    
    def generate_detailed_report(self):
        """Generate a detailed validation report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"model_validation_report_{timestamp}.json"
        
        report = {
            'validation_date': datetime.now().isoformat(),
            'model_path': self.model_path,
            'total_test_events': len(self.test_events),
            'test_results': self.results,
            'summary': {
                'bert_available': any(r['bert_prediction']['priority'] is not None for r in self.results),
                'fallback_available': any(r['fallback_prediction']['priority'] is not None for r in self.results),
                'bert_accuracy': sum(1 for r in self.results if r['bert_prediction']['correct']) / len(self.results) * 100,
                'fallback_accuracy': sum(1 for r in self.results if r['fallback_prediction']['correct']) / len(self.results) * 100
            }
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"\n💾 Detailed report saved to: {report_file}")
        except Exception as e:
            logger.error(f"⚠️ Failed to save detailed report: {e}")
        
        return report
    
    def run_validation(self):
        """Run complete validation process"""
        logger.info("🔍 KairoCal BERT Model Post-Training Validation")
        logger.info("=" * 80)
        logger.info(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"📊 Test events: {len(self.test_events)}")
        
        # Load models
        bert_classifier = self.load_trained_model()
        fallback_system = self.load_fallback_system()
        
        if not bert_classifier and not fallback_system:
            logger.error("❌ No models available for testing!")
            return False
        
        # Run tests
        summary = self.test_model_predictions(bert_classifier, fallback_system)
        
        # Analyze results
        self.analyze_confidence_scores()
        self.check_model_improvement()
        
        # Generate report
        report = self.generate_detailed_report()
        
        # Final assessment
        logger.info("\n" + "=" * 80)
        logger.info("🎯 VALIDATION ASSESSMENT")
        logger.info("=" * 80)
        
        if bert_classifier and bert_classifier.is_trained:
            logger.info("✅ Trained BERT model successfully loaded and tested")
            if summary['bert_accuracy'] >= 50:
                logger.info("✅ Model performance is acceptable for production")
            elif summary['bert_accuracy'] >= 30:
                logger.info("⚠️ Model performance is moderate, consider additional training")
            else:
                logger.info("❌ Model performance is low, requires retraining")
        else:
            logger.info("❌ Trained BERT model not available or not properly loaded")
        
        if summary['bert_accuracy'] > summary['fallback_accuracy']:
            logger.info("🏆 BERT model outperforms rule-based fallback")
        else:
            logger.info("⚠️ Rule-based fallback performs as well or better than BERT")
        
        logger.info(f"\n📋 Next Steps:")
        if bert_classifier and bert_classifier.is_trained:
            logger.info("  1. ✅ BERT model is ready for integration testing")
            logger.info("  2. 🔄 Proceed to Task 4: Update Model Loading")
            logger.info("  3. 🧪 Proceed to Task 5: Final System Test")
        else:
            logger.info("  1. ❌ Fix BERT model loading issues")
            logger.info("  2. 🔄 Retrain model if necessary")
            logger.info("  3. ⚠️ Use fallback system until BERT is ready")
        
        return bert_classifier is not None and bert_classifier.is_trained

def main():
    """Main validation entry point"""
    validator = TrainedModelValidator()
    success = validator.run_validation()
    
    if success:
        logger.info("\n🎉 Model validation completed successfully!")
        sys.exit(0)
    else:
        logger.error("\n❌ Model validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
