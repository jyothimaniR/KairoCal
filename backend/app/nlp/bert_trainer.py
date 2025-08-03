# backend/app/nlp/bert_trainer.py
"""
BERT Priority Model Training Pipeline
Fine-tunes DistilBERT for event priority classification with advanced features
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import (
    DistilBertTokenizer, 
    DistilBertModel,
    AdamW,
    get_linear_schedule_with_warmup
)
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
import logging
import os
from datetime import datetime
import json
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from .bert_priority_classifier import AdvancedEventPriorityClassifier
from .bert_training_data_generator import BERTTrainingDataGenerator

logger = logging.getLogger(__name__)

class EventPriorityDataset(Dataset):
    """PyTorch Dataset for event priority classification"""
    
    def __init__(self, 
                 examples: List[Dict[str, Any]], 
                 tokenizer: DistilBertTokenizer,
                 classifier: AdvancedEventPriorityClassifier,
                 max_length: int = 128):
        self.examples = examples
        self.tokenizer = tokenizer
        self.classifier = classifier
        self.max_length = max_length
        
    def __len__(self):
        return len(self.examples)
        
    def __getitem__(self, idx):
        example = self.examples[idx]
        
        # Prepare text
        title = example.get('title', '')
        description = example.get('description', '')
        text = f"{title}. {description}".strip()
        
        # Tokenize text
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        # Extract additional features using the classifier
        _, feature_tensor = self.classifier._combine_features(example)
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'features': feature_tensor.flatten(),
            'labels': torch.tensor(example['priority'] - 1, dtype=torch.long)  # 0-4 for PyTorch
        }

class BERTPriorityTrainer:
    """
    Comprehensive trainer for BERT priority classification
    
    Features:
    - Advanced training loop with validation
    - Learning rate scheduling
    - Early stopping
    - Comprehensive evaluation
    - Model checkpointing
    """
    
    def __init__(self, 
                 model_save_path: str = "models/bert_priority_classifier.pt",
                 device: str = None):
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_save_path = model_save_path
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        
        # Training history
        self.training_history = {
            'train_loss': [],
            'val_loss': [],
            'val_accuracy': [],
            'learning_rates': []
        }
        
        # Ensure model directory exists
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        
    def prepare_data(self, 
                    training_examples: List[Dict[str, Any]], 
                    validation_split: float = 0.2) -> Tuple[DataLoader, DataLoader]:
        """Prepare training and validation data loaders"""
        
        # Split the data
        train_examples, val_examples = train_test_split(
            training_examples, 
            test_size=validation_split, 
            stratify=[ex['priority'] for ex in training_examples],
            random_state=42
        )
        
        logger.info(f"Training examples: {len(train_examples)}")
        logger.info(f"Validation examples: {len(val_examples)}")
        
        # Create classifier instance for feature extraction
        classifier = AdvancedEventPriorityClassifier()
        
        # Create datasets
        train_dataset = EventPriorityDataset(train_examples, self.tokenizer, classifier)
        val_dataset = EventPriorityDataset(val_examples, self.tokenizer, classifier)
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=16, 
            shuffle=True,
            num_workers=0  # Set to 0 for compatibility
        )
        
        val_loader = DataLoader(
            val_dataset, 
            batch_size=32, 
            shuffle=False,
            num_workers=0
        )
        
        return train_loader, val_loader
        
    def create_model(self) -> Tuple[DistilBertModel, nn.Module]:
        """Create the BERT model and classifier"""
        # Load pre-trained DistilBERT
        bert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')
        
        # Create classifier head
        classifier = nn.Sequential(
            nn.Linear(768 + 64, 256),  # BERT embeddings + features
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 5)  # 5 priority classes
        )
        
        # Move to device
        bert_model.to(self.device)
        classifier.to(self.device)
        
        return bert_model, classifier
        
    def train_epoch(self, 
                   model: Tuple[DistilBertModel, nn.Module], 
                   train_loader: DataLoader, 
                   optimizer, 
                   scheduler,
                   criterion) -> float:
        """Train for one epoch"""
        bert_model, classifier = model
        bert_model.train()
        classifier.train()
        
        total_loss = 0
        num_batches = 0
        
        progress_bar = tqdm(train_loader, desc="Training")
        
        for batch in progress_bar:
            # Move batch to device
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            features = batch['features'].to(self.device)
            labels = batch['labels'].to(self.device)
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Forward pass through BERT
            bert_outputs = bert_model(input_ids=input_ids, attention_mask=attention_mask)
            bert_embeddings = bert_outputs.last_hidden_state[:, 0, :]  # [CLS] token
            
            # Combine BERT embeddings with features
            combined_input = torch.cat([bert_embeddings, features], dim=1)
            
            # Forward pass through classifier
            logits = classifier(combined_input)
            
            # Calculate loss
            loss = criterion(logits, labels)
            
            # Backward pass
            loss.backward()
            
            # Clip gradients to prevent exploding gradients
            torch.nn.utils.clip_grad_norm_(bert_model.parameters(), 1.0)
            torch.nn.utils.clip_grad_norm_(classifier.parameters(), 1.0)
            
            # Update weights
            optimizer.step()
            scheduler.step()
            
            total_loss += loss.item()
            num_batches += 1
            
            # Update progress bar
            progress_bar.set_postfix({'loss': loss.item()})
            
        return total_loss / num_batches
        
    def validate(self, 
                model: Tuple[DistilBertModel, nn.Module], 
                val_loader: DataLoader, 
                criterion) -> Tuple[float, float, List[int], List[int]]:
        """Validate the model"""
        bert_model, classifier = model
        bert_model.eval()
        classifier.eval()
        
        total_loss = 0
        num_batches = 0
        all_predictions = []
        all_labels = []
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Validation"):
                # Move batch to device
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                features = batch['features'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                # Forward pass
                bert_outputs = bert_model(input_ids=input_ids, attention_mask=attention_mask)
                bert_embeddings = bert_outputs.last_hidden_state[:, 0, :]
                combined_input = torch.cat([bert_embeddings, features], dim=1)
                logits = classifier(combined_input)
                
                # Calculate loss
                loss = criterion(logits, labels)
                total_loss += loss.item()
                num_batches += 1
                
                # Get predictions
                predictions = torch.argmax(logits, dim=1)
                all_predictions.extend(predictions.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                
        avg_loss = total_loss / num_batches
        accuracy = accuracy_score(all_labels, all_predictions)
        
        return avg_loss, accuracy, all_predictions, all_labels
        
    def train(self, 
             training_examples: List[Dict[str, Any]], 
             num_epochs: int = 10,
             learning_rate: float = 2e-5,
             validation_split: float = 0.2,
             early_stopping_patience: int = 3) -> Dict[str, Any]:
        """
        Main training loop
        
        Args:
            training_examples: List of training examples
            num_epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
            validation_split: Fraction of data to use for validation
            early_stopping_patience: Epochs to wait before early stopping
            
        Returns:
            Training results and metrics
        """
        logger.info("Starting BERT Priority Classification Training")
        logger.info(f"Device: {self.device}")
        logger.info(f"Training examples: {len(training_examples)}")
        
        # Prepare data
        train_loader, val_loader = self.prepare_data(training_examples, validation_split)
        
        # Create model
        bert_model, classifier = self.create_model()
        
        # Setup optimizer and scheduler
        optimizer = AdamW(
            list(bert_model.parameters()) + list(classifier.parameters()),
            lr=learning_rate,
            weight_decay=0.01
        )
        
        total_steps = len(train_loader) * num_epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=int(0.1 * total_steps),
            num_training_steps=total_steps
        )
        
        # Loss function with class weights (optional)
        criterion = nn.CrossEntropyLoss()
        
        # Training loop
        best_val_accuracy = 0
        patience_counter = 0
        
        for epoch in range(num_epochs):
            logger.info(f"\nEpoch {epoch + 1}/{num_epochs}")
            
            # Train
            train_loss = self.train_epoch(
                (bert_model, classifier), 
                train_loader, 
                optimizer, 
                scheduler, 
                criterion
            )
            
            # Validate
            val_loss, val_accuracy, val_predictions, val_labels = self.validate(
                (bert_model, classifier), 
                val_loader, 
                criterion
            )
            
            # Record training history
            self.training_history['train_loss'].append(train_loss)
            self.training_history['val_loss'].append(val_loss)
            self.training_history['val_accuracy'].append(val_accuracy)
            self.training_history['learning_rates'].append(optimizer.param_groups[0]['lr'])
            
            logger.info(f"Train Loss: {train_loss:.4f}")
            logger.info(f"Val Loss: {val_loss:.4f}")
            logger.info(f"Val Accuracy: {val_accuracy:.4f}")
            
            # Early stopping check
            if val_accuracy > best_val_accuracy:
                best_val_accuracy = val_accuracy
                patience_counter = 0
                
                # Save best model
                self.save_model(bert_model, classifier, 
                              f"{self.model_save_path}_best.pt")
                logger.info(f"New best model saved with accuracy: {val_accuracy:.4f}")
            else:
                patience_counter += 1
                
            if patience_counter >= early_stopping_patience:
                logger.info(f"Early stopping triggered after {epoch + 1} epochs")
                break
                
        # Save final model
        self.save_model(bert_model, classifier, self.model_save_path)
        
        # Generate final evaluation
        final_results = self.evaluate_model(
            (bert_model, classifier), 
            val_loader, 
            val_predictions, 
            val_labels
        )
        
        logger.info("Training completed!")
        return final_results
        
    def save_model(self, 
                  bert_model: DistilBertModel, 
                  classifier: nn.Module, 
                  path: str):
        """Save the trained model"""
        checkpoint = {
            'bert_model': bert_model.state_dict(),
            'classifier': classifier.state_dict(),
            'training_history': self.training_history,
            'model_config': {
                'bert_model_name': 'distilbert-base-uncased',
                'num_classes': 5,
                'feature_dim': 64
            }
        }
        torch.save(checkpoint, path)
        logger.info(f"Model saved to {path}")
        
    def evaluate_model(self, 
                      model: Tuple[DistilBertModel, nn.Module], 
                      val_loader: DataLoader,
                      predictions: List[int], 
                      labels: List[int]) -> Dict[str, Any]:
        """Comprehensive model evaluation"""
        
        # Convert back to 1-5 priority scale for reporting
        predictions_priority = [p + 1 for p in predictions]
        labels_priority = [l + 1 for l in labels]
        
        # Classification report
        class_names = ['Very Low', 'Low', 'Medium', 'High', 'Critical']
        report = classification_report(
            labels_priority, 
            predictions_priority,
            target_names=class_names,
            output_dict=True
        )
        
        # Confusion matrix
        cm = confusion_matrix(labels_priority, predictions_priority)
        
        # Overall accuracy
        accuracy = accuracy_score(labels_priority, predictions_priority)
        
        results = {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'training_history': self.training_history,
            'class_names': class_names
        }
        
        # Print results
        logger.info(f"Final Model Accuracy: {accuracy:.4f}")
        logger.info("\nClassification Report:")
        logger.info(classification_report(labels_priority, predictions_priority, target_names=class_names))
        
        return results