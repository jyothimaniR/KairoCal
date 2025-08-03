# backend/app/scripts/train_bert_priority_model.py
"""
Training Script for BERT Priority Classification Model
Generates training data and trains the BERT model for event priority classification
"""

import os
import sys
import logging
from datetime import datetime
import json

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.nlp.bert_trainer import BERTPriorityTrainer
from app.nlp.bert_training_data_generator import BERTTrainingDataGenerator
from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'bert_training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main training pipeline"""
    logger.info("🚀 Starting BERT Priority Classification Model Training")
    
    # Configuration
    config = {
        'training_size': 2000,
        'validation_split': 0.2,
        'num_epochs': 10,
        'learning_rate': 2e-5,
        'early_stopping_patience': 3,
        'model_save_path': 'models/bert_priority_classifier.pt',
        'balanced_dataset': True
    }
    
    logger.info(f"Training Configuration: {json.dumps(config, indent=2)}")
    
    try:
        # Step 1: Generate Training Data
        logger.info("📊 Step 1: Generating training data...")
        data_generator = BERTTrainingDataGenerator()
        
        training_examples = data_generator.generate_training_dataset(
            size=config['training_size'],
            balanced=config['balanced_dataset']
        )
        
        logger.info(f"Generated {len(training_examples)} training examples")
        
        # Analyze dataset quality
        dataset_analysis = data_generator.analyze_dataset(training_examples)
        logger.info(f"Dataset Analysis: {json.dumps(dataset_analysis, indent=2)}")
        
        # Save training data for future reference
        training_data_path = f"data/bert_training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(training_data_path), exist_ok=True)
        data_generator.save_training_data(training_examples, training_data_path)
        logger.info(f"Training data saved to: {training_data_path}")
        
        # Step 2: Initialize Trainer
        logger.info("🤖 Step 2: Initializing BERT trainer...")
        trainer = BERTPriorityTrainer(model_save_path=config['model_save_path'])
        
        # Step 3: Train Model
        logger.info("🎯 Step 3: Training BERT model...")
        training_results = trainer.train(
            training_examples=training_examples,
            num_epochs=config['num_epochs'],
            learning_rate=config['learning_rate'],
            validation_split=config['validation_split'],
            early_stopping_patience=config['early_stopping_patience']
        )
        
        logger.info("✅ Training completed successfully!")
        
        # Step 4: Save Training Results
        results_path = f"results/bert_training_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        with open(results_path, 'w') as f:
            json.dump(training_results, f, indent=2, default=str)
        logger.info(f"Training results saved to: {results_path}")
        
        # Step 5: Validate with Test Scenarios
        logger.info("🧪 Step 5: Validating with test scenarios...")
        validate_trained_model(config['model_save_path'] + "_best.pt", data_generator)
        
        logger.info("🎉 BERT Priority Classification Model Training Complete!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Training failed: {str(e)}")
        return False

def validate_trained_model(model_path: str, data_generator: BERTTrainingDataGenerator):
    """Validate the trained model with specific test scenarios"""
    try:
        # Load trained model
        classifier = AdvancedEventPriorityClassifier(model_path)
        
        # Generate validation scenarios
        validation_scenarios = data_generator.generate_validation_scenarios()
        
        logger.info("🔍 Testing model on validation scenarios:")
        correct_predictions = 0
        total_predictions = len(validation_scenarios)
        
        for scenario in validation_scenarios:
            expected_priority = scenario.pop('expected_priority')
            predicted_priority, confidence = classifier.predict(scenario)
            
            is_correct = predicted_priority == expected_priority
            correct_predictions += is_correct
            
            status = "✅" if is_correct else "❌"
            logger.info(
                f"{status} Event: '{scenario['title'][:50]}...' | "
                f"Expected: {expected_priority} | Predicted: {predicted_priority} | "
                f"Confidence: {confidence:.3f}"
            )
            
        accuracy = correct_predictions / total_predictions
        logger.info(f"🎯 Validation Accuracy: {accuracy:.1%} ({correct_predictions}/{total_predictions})")
        
        # Test edge cases
        test_edge_cases(classifier)
        
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")

def test_edge_cases(classifier: AdvancedEventPriorityClassifier):
    """Test the model with edge cases and unusual inputs"""
    logger.info("🔬 Testing edge cases...")
    
    edge_cases = [
        {
            "title": "URGENT URGENT URGENT CEO EMERGENCY",
            "description": "CRITICAL CRITICAL CRITICAL",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "expected_priority": 5
        },
        {
            "title": "coffee",
            "description": "optional casual break",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(minutes=15)).isoformat(),
            "expected_priority": 1
        },
        {
            "title": "",
            "description": "",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "expected_priority": 3  # Should default to medium
        }
    ]
    
    for i, case in enumerate(edge_cases):
        expected = case.pop('expected_priority')
        predicted, confidence = classifier.predict(case)
        
        logger.info(f"Edge Case {i+1}: Expected {expected}, Got {predicted} (confidence: {confidence:.3f})")

if __name__ == "__main__":
    from datetime import timedelta
    
    # Ensure required directories exist
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    success = main()
    exit(0 if success else 1)