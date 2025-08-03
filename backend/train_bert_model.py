# backend/train_bert_model.py
"""
BERT Priority Classifier Training Script
Trains the event priority classification model using synthetic data
"""

import sys
import os
import torch
import json
import logging
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
from app.nlp.bert_training_data_generator import BERTTrainingDataGenerator
from app.config import get_settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bert_training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BERTModelTrainer:
    """Comprehensive BERT model training pipeline"""
    
    def __init__(self):
        self.settings = get_settings()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.training_start_time = None
        self.model_save_path = self.settings.bert_model_path
        
        # Create necessary directories
        os.makedirs(self.model_save_path, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs(self.settings.training_data_path, exist_ok=True)
        
        logger.info(f"🤖 BERT Training initialized on device: {self.device}")
        logger.info(f"📁 Model will be saved to: {self.model_save_path}")
        
    def generate_training_data(self, dataset_size: int = 2000) -> tuple:
        """Generate comprehensive training dataset"""
        logger.info(f"📊 Generating {dataset_size} training examples...")
        
        data_generator = BERTTrainingDataGenerator()
        
        # Generate balanced dataset
        training_examples = data_generator.generate_training_dataset(
            size=dataset_size, 
            balanced=True
        )
        
        # Save raw training data for analysis
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_file = f"{self.settings.training_data_path}/training_data_{timestamp}.json"
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(training_examples, f, indent=2, default=str)
            
        logger.info(f"💾 Training data saved to: {data_file}")
        
        # Extract features and labels
        texts = []
        labels = []
        
        for example in training_examples:
            # Combine title and description for text input
            text = f"{example['title']} {example.get('description', '')}"
            texts.append(text.strip())
            labels.append(example['priority'])  # Keep 1-5 range for BERT training method
            
        return texts, labels, training_examples
        
    def split_data(self, texts: list, labels: list, test_size: float = 0.2):
        """Split data into training and validation sets"""
        logger.info(f"🔄 Splitting data: {100*(1-test_size):.0f}% train, {100*test_size:.0f}% validation")
        
        X_train, X_val, y_train, y_val = train_test_split(
            texts, labels, 
            test_size=test_size, 
            random_state=42, 
            stratify=labels
        )
        
        logger.info(f"📈 Training samples: {len(X_train)}")
        logger.info(f"📊 Validation samples: {len(X_val)}")
        
        # Log class distribution
        unique_train, counts_train = np.unique(y_train, return_counts=True)
        unique_val, counts_val = np.unique(y_val, return_counts=True)
        
        logger.info("📊 Training class distribution:")
        for cls, count in zip(unique_train, counts_train):
            logger.info(f"   Priority {cls+1}: {count} samples")
            
        logger.info("📊 Validation class distribution:")
        for cls, count in zip(unique_val, counts_val):
            logger.info(f"   Priority {cls+1}: {count} samples")
            
        return X_train, X_val, y_train, y_val
        
    def train_model(self, X_train: list, y_train: list, X_val: list, y_val: list, 
                   epochs: int = 3, learning_rate: float = 2e-5):
        """Train the BERT classifier"""
        logger.info(f"🚀 Starting BERT training for {epochs} epochs...")
        self.training_start_time = datetime.now()
        
        # Initialize classifier
        classifier = AdvancedEventPriorityClassifier()
        
        try:
            # Train the model
            training_history = classifier.train(
                X_train, y_train, 
                X_val, y_val,
                epochs=epochs,
                learning_rate=learning_rate,
                batch_size=self.settings.batch_size
            )
            
            logger.info("✅ Training completed successfully!")
            return classifier, training_history
            
        except Exception as e:
            logger.error(f"❌ Training failed: {str(e)}")
            raise
            
    def evaluate_model(self, classifier, X_val: list, y_val: list):
        """Evaluate model performance"""
        logger.info("📊 Evaluating model performance...")
        
        # Get predictions
        predictions = []
        confidences = []
        
        for text in X_val:
            # Create event dict for prediction
            event_data = {"title": text, "description": ""}
            priority, confidence = classifier.predict(event_data)
            predictions.append(priority - 1)  # Convert back to 0-4 range
            confidences.append(confidence)
            
        # Calculate metrics
        accuracy = accuracy_score(y_val, predictions)
        avg_confidence = np.mean(confidences)
        
        logger.info(f"🎯 Validation Accuracy: {accuracy:.4f}")
        logger.info(f"🔍 Average Confidence: {avg_confidence:.4f}")
        
        # Detailed classification report
        priority_names = ['Very Low', 'Low', 'Medium', 'High', 'Critical']
        unique_classes = sorted(set(y_val))
        
        # Ensure we have proper labels for classification report
        labels = list(range(len(priority_names)))
        report = classification_report(y_val, predictions, target_names=priority_names, labels=labels, zero_division=0)
        logger.info(f"📋 Classification Report:\n{report}")
        
        # Confusion matrix
        cm = confusion_matrix(y_val, predictions)
        logger.info(f"🔢 Confusion Matrix:\n{cm}")
        
        return {
            'accuracy': accuracy,
            'average_confidence': avg_confidence,
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'predictions': predictions,
            'confidences': confidences
        }
        
    def save_model_and_metrics(self, classifier, training_history: dict, evaluation_metrics: dict):
        """Save trained model and performance metrics"""
        logger.info(f"💾 Saving model to: {self.model_save_path}")
        
        try:
            # Save the model
            classifier.save_model(self.model_save_path)
            
            # Save training metadata
            metadata = {
                'training_date': datetime.now().isoformat(),
                'training_duration_minutes': (datetime.now() - self.training_start_time).total_seconds() / 60,
                'device': str(self.device),
                'model_config': {
                    'batch_size': self.settings.batch_size,
                    'max_sequence_length': self.settings.max_sequence_length,
                    'priority_levels': self.settings.priority_levels,
                    'confidence_threshold': self.settings.model_confidence_threshold
                },
                'training_history': training_history,
                'evaluation_metrics': evaluation_metrics
            }
            
            metadata_file = f"{self.model_save_path}/training_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, default=str)
                
            logger.info(f"📊 Training metadata saved to: {metadata_file}")
            logger.info("✅ Model and metadata saved successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to save model: {str(e)}")
            raise
            
    def test_sample_predictions(self, classifier):
        """Test model on sample events"""
        logger.info("🧪 Testing model on sample events...")
        
        sample_events = [
            {
                "title": "URGENT: CEO Emergency Meeting",
                "description": "Critical business decision required immediately",
                "expected_priority": 5
            },
            {
                "title": "Team Coffee Break", 
                "description": "Casual team gathering",
                "expected_priority": 1
            },
            {
                "title": "Client Presentation",
                "description": "Important quarterly review with major client",
                "expected_priority": 4
            },
            {
                "title": "Weekly Team Standup",
                "description": "Regular team sync meeting",
                "expected_priority": 3
            },
            {
                "title": "Optional Training Workshop",
                "description": "Skills development session",
                "expected_priority": 2
            }
        ]
        
        logger.info("🎯 Sample Predictions:")
        correct_predictions = 0
        
        for event in sample_events:
            priority, confidence = classifier.predict(event)
            is_correct = priority == event["expected_priority"]
            if is_correct:
                correct_predictions += 1
                
            status = "✅" if is_correct else "❌"
            logger.info(f"   {status} '{event['title'][:40]}...' → Priority: {priority} (Expected: {event['expected_priority']}), Confidence: {confidence:.3f}")
            
        sample_accuracy = correct_predictions / len(sample_events)
        logger.info(f"🎯 Sample Test Accuracy: {sample_accuracy:.2%}")
        
    def run_full_training_pipeline(self, dataset_size: int = 2000, epochs: int = 3):
        """Execute complete training pipeline"""
        logger.info("🚀 Starting BERT Priority Classifier Training Pipeline")
        logger.info("=" * 60)
        
        try:
            # Step 1: Generate training data
            texts, labels, raw_data = self.generate_training_data(dataset_size)
            
            # Step 2: Split data
            X_train, X_val, y_train, y_val = self.split_data(texts, labels)
            
            # Step 3: Train model
            classifier, training_history = self.train_model(X_train, y_train, X_val, y_val, epochs)
            
            # Step 4: Evaluate model
            evaluation_metrics = self.evaluate_model(classifier, X_val, y_val)
            
            # Step 5: Save model and metrics
            self.save_model_and_metrics(classifier, training_history, evaluation_metrics)
            
            # Step 6: Test sample predictions
            self.test_sample_predictions(classifier)
            
            # Final summary
            training_duration = (datetime.now() - self.training_start_time).total_seconds() / 60
            logger.info("=" * 60)
            logger.info("🎉 TRAINING COMPLETED SUCCESSFULLY!")
            logger.info(f"⏱️ Total Training Time: {training_duration:.2f} minutes")
            logger.info(f"🎯 Final Validation Accuracy: {evaluation_metrics['accuracy']:.4f}")
            logger.info(f"🔍 Average Confidence: {evaluation_metrics['average_confidence']:.4f}")
            logger.info(f"💾 Model saved to: {self.model_save_path}")
            logger.info("=" * 60)
            
            return classifier, evaluation_metrics
            
        except Exception as e:
            logger.error(f"❌ Training pipeline failed: {str(e)}")
            raise

def main():
    """Main training script entry point"""
    print("🤖 KairoCal BERT Priority Classifier Training")
    print("=" * 60)
    
    # Parse command line arguments (basic)
    dataset_size = 2000
    epochs = 3
    
    if len(sys.argv) > 1:
        try:
            dataset_size = int(sys.argv[1])
        except ValueError:
            print("⚠️ Invalid dataset size, using default: 2000")
            
    if len(sys.argv) > 2:
        try: 
            epochs = int(sys.argv[2])
        except ValueError:
            print("⚠️ Invalid epochs, using default: 3")
    
    print(f"📊 Dataset Size: {dataset_size}")
    print(f"🔄 Training Epochs: {epochs}")
    print()
    
    # Initialize and run trainer
    trainer = BERTModelTrainer()
    
    try:
        classifier, metrics = trainer.run_full_training_pipeline(
            dataset_size=dataset_size, 
            epochs=epochs
        )
        
        print("\n🎉 Training completed successfully!")
        print(f"🎯 Final Accuracy: {metrics['accuracy']:.4f}")
        print("\n✅ You can now use the trained BERT model in your KairoCal application!")
        
    except Exception as e:
        print(f"\n❌ Training failed: {str(e)}")
        logger.error(f"Training failed with error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
