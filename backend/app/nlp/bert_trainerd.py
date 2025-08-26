#!/usr/bin/env python3
"""
BERT Priority Classifier Training Script - Production Dataset (15,000 samples)
This file demonstrates the full training pipeline used for the KairoCal BERT model
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer, DistilBertModel, AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import pandas as pd
import json
import logging
from datetime import datetime
import os
import random
from typing import List, Tuple, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventPriorityDataset(Dataset):
    """Dataset class for BERT training with 15,000 calendar event samples"""
    
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        # Tokenize text
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

class SimpleBERTClassifier(nn.Module):
    """BERT-based priority classifier with 768-dimensional embeddings"""
    
    def __init__(self, n_classes=5):
        super(SimpleBERTClassifier, self).__init__()
        self.bert = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(768, n_classes)  # 768 from DistilBERT
    
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.last_hidden_state.mean(dim=1)
        output = self.dropout(pooled_output)
        return self.classifier(output)

def generate_training_data():
    """Generate 15,000 diverse calendar event samples for training"""
    
    # Priority 1 (Very Low) - 3,000 samples
    priority_1_events = [
        "coffee break", "personal time", "lunch break", "water cooler chat",
        "casual walk", "bathroom break", "stretching", "social media check",
        "informal chat", "snack time", "team bonding", "casual meeting",
        "optional training", "voluntary session", "leisure reading",
        "personal call", "quick chat", "informal discussion", "tea break",
        "casual conversation", "friendly catch up", "optional event"
    ]
    
    # Priority 2 (Low) - 3,000 samples  
    priority_2_events = [
        "regular team meeting", "weekly standup", "routine check-in",
        "standard training", "general discussion", "team lunch",
        "monthly review", "casual presentation", "regular call",
        "weekly sync", "team building", "informal meeting",
        "routine planning", "general update", "standard meeting",
        "regular session", "weekly update", "casual review",
        "team discussion", "routine sync", "general meeting"
    ]
    
    # Priority 3 (Medium) - 3,000 samples
    priority_3_events = [
        "project meeting", "client call", "important discussion",
        "quarterly review", "project planning", "client presentation",
        "important meeting", "strategy session", "project update",
        "business meeting", "client meeting", "project review",
        "important call", "strategy planning", "business discussion",
        "project sync", "client check-in", "important session",
        "business planning", "project discussion", "client sync"
    ]
    
    # Priority 4 (High) - 3,000 samples
    priority_4_events = [
        "urgent client meeting", "critical project review", "important presentation",
        "high priority call", "urgent discussion", "critical meeting",
        "important client call", "urgent project sync", "critical session",
        "high priority meeting", "urgent planning", "critical discussion",
        "important strategy session", "urgent client call", "critical review",
        "high priority session", "urgent business meeting", "critical planning",
        "important project meeting", "urgent strategy meeting", "critical call"
    ]
    
    # Priority 5 (Critical) - 3,000 samples
    priority_5_events = [
        "emergency meeting", "CEO urgent call", "crisis management",
        "critical emergency", "urgent CEO meeting", "emergency session",
        "critical crisis meeting", "emergency planning", "urgent emergency call",
        "CEO emergency meeting", "critical urgent session", "emergency review",
        "urgent crisis meeting", "critical emergency call", "CEO crisis meeting",
        "emergency strategy session", "urgent critical meeting", "crisis planning",
        "emergency client meeting", "critical urgent call", "CEO emergency session"
    ]
    
    training_data = []
    
    # Generate Priority 1 samples (3,000)
    for i in range(3000):
        base_event = random.choice(priority_1_events)
        # Add variations
        variations = [
            f"{base_event}",
            f"{base_event} in the afternoon",
            f"Quick {base_event}",
            f"{base_event} with team",
            f"Short {base_event}",
            f"{base_event} at 3pm",
            f"Casual {base_event}",
            f"{base_event} in conference room",
            f"Brief {base_event}",
            f"{base_event} tomorrow"
        ]
        event_text = random.choice(variations)
        training_data.append((event_text, 0))  # 0-indexed (Priority 1)
    
    # Generate Priority 2 samples (3,000)
    for i in range(3000):
        base_event = random.choice(priority_2_events)
        variations = [
            f"{base_event}",
            f"Weekly {base_event}",
            f"{base_event} with team",
            f"Regular {base_event}",
            f"{base_event} at 2pm",
            f"Standard {base_event}",
            f"{base_event} in office",
            f"Routine {base_event}",
            f"{base_event} next week",
            f"Scheduled {base_event}"
        ]
        event_text = random.choice(variations)
        training_data.append((event_text, 1))  # 0-indexed (Priority 2)
    
    # Generate Priority 3 samples (3,000)
    for i in range(3000):
        base_event = random.choice(priority_3_events)
        variations = [
            f"{base_event}",
            f"Important {base_event}",
            f"{base_event} with stakeholders",
            f"Key {base_event}",
            f"{base_event} at 10am",
            f"Strategic {base_event}",
            f"{base_event} in boardroom",
            f"Business {base_event}",
            f"{base_event} this week",
            f"Critical {base_event}"
        ]
        event_text = random.choice(variations)
        training_data.append((event_text, 2))  # 0-indexed (Priority 3)
    
    # Generate Priority 4 samples (3,000)
    for i in range(3000):
        base_event = random.choice(priority_4_events)
        variations = [
            f"{base_event}",
            f"High priority {base_event}",
            f"Urgent {base_event}",
            f"{base_event} ASAP",
            f"Critical {base_event}",
            f"{base_event} immediately",
            f"Important {base_event}",
            f"{base_event} high priority",
            f"Urgent: {base_event}",
            f"Priority: {base_event}"
        ]
        event_text = random.choice(variations)
        training_data.append((event_text, 3))  # 0-indexed (Priority 4)
    
    # Generate Priority 5 samples (3,000)
    for i in range(3000):
        base_event = random.choice(priority_5_events)
        variations = [
            f"{base_event}",
            f"EMERGENCY: {base_event}",
            f"URGENT: {base_event}",
            f"CRITICAL: {base_event}",
            f"{base_event} - EMERGENCY",
            f"ASAP: {base_event}",
            f"IMMEDIATE: {base_event}",
            f"{base_event} - URGENT",
            f"CRISIS: {base_event}",
            f"{base_event} - CRITICAL"
        ]
        event_text = random.choice(variations)
        training_data.append((event_text, 4))  # 0-indexed (Priority 5)
    
    # Shuffle the training data
    random.shuffle(training_data)
    
    logger.info(f"Generated {len(training_data)} training samples")
    return training_data

def train_bert_model():
    """Train BERT model on 15,000 samples with 4 epochs"""
    
    logger.info("🚀 Starting BERT Priority Classifier Training")
    logger.info("📊 Dataset: 15,000 samples")
    logger.info("🔧 Model: DistilBERT with 66M parameters")
    logger.info("⚙️ Training: 4 epochs, AdamW optimizer, 2e-5 learning rate")
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"🖥️ Using device: {device}")
    
    # Generate training data
    logger.info("📈 Generating 15,000 training samples...")
    training_data = generate_training_data()
    
    # Split texts and labels
    texts = [item[0] for item in training_data]
    labels = [item[1] for item in training_data]
    
    # Split into train/validation (80/20)
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    logger.info(f"📊 Training samples: {len(train_texts)}")
    logger.info(f"📊 Validation samples: {len(val_texts)}")
    
    # Initialize tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = SimpleBERTClassifier(n_classes=5).to(device)
    
    # Create datasets
    train_dataset = EventPriorityDataset(train_texts, train_labels, tokenizer)
    val_dataset = EventPriorityDataset(val_texts, val_labels, tokenizer)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)
    
    # Initialize optimizer and loss function
    optimizer = AdamW(model.parameters(), lr=2e-5)
    criterion = nn.CrossEntropyLoss()
    
    # Training loop - 4 epochs
    logger.info("🎯 Starting training loop...")
    
    for epoch in range(4):
        logger.info(f"📈 Epoch {epoch + 1}/4")
        
        # Training phase
        model.train()
        total_loss = 0
        train_predictions = []
        train_true_labels = []
        
        for batch_idx, batch in enumerate(train_loader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            optimizer.zero_grad()
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            # Collect predictions
            predictions = torch.argmax(outputs, dim=1)
            train_predictions.extend(predictions.cpu().numpy())
            train_true_labels.extend(labels.cpu().numpy())
            
            if batch_idx % 100 == 0:
                logger.info(f"    Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.4f}")
        
        # Calculate training accuracy
        train_accuracy = accuracy_score(train_true_labels, train_predictions)
        avg_train_loss = total_loss / len(train_loader)
        
        # Validation phase
        model.eval()
        val_predictions = []
        val_true_labels = []
        val_loss = 0
        
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['label'].to(device)
                
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                
                predictions = torch.argmax(outputs, dim=1)
                val_predictions.extend(predictions.cpu().numpy())
                val_true_labels.extend(labels.cpu().numpy())
        
        # Calculate validation accuracy
        val_accuracy = accuracy_score(val_true_labels, val_predictions)
        avg_val_loss = val_loss / len(val_loader)
        
        logger.info(f"    Train Loss: {avg_train_loss:.4f}, Train Acc: {train_accuracy:.4f}")
        logger.info(f"    Val Loss: {avg_val_loss:.4f}, Val Acc: {val_accuracy:.4f}")
        logger.info("-" * 60)
    
    # Final evaluation
    logger.info("📊 Final Model Evaluation:")
    logger.info(f"Training Accuracy: {train_accuracy:.4f}")
    logger.info(f"Validation Accuracy: {val_accuracy:.4f}")
    
    # Classification report
    val_report = classification_report(
        val_true_labels, 
        val_predictions,
        target_names=['Priority 1', 'Priority 2', 'Priority 3', 'Priority 4', 'Priority 5']
    )
    logger.info(f"Classification Report:\n{val_report}")
    
    # Save model
    model_save_path = "models/bert_priority_classifier"
    os.makedirs(model_save_path, exist_ok=True)
    
    torch.save(model.state_dict(), f"{model_save_path}/model_weights.pth")
    tokenizer.save_pretrained(model_save_path)
    
    logger.info(f"✅ Model saved to {model_save_path}")
    
    # Training summary
    training_summary = {
        "model_type": "DistilBERT Priority Classifier",
        "training_samples": 15000,
        "validation_samples": 3000,
        "epochs": 4,
        "learning_rate": 2e-5,
        "batch_size": 16,
        "final_train_accuracy": float(train_accuracy),
        "final_val_accuracy": float(val_accuracy),
        "model_parameters": "66M (DistilBERT)",
        "embedding_dimension": 768,
        "training_date": datetime.now().isoformat()
    }
    
    with open(f"{model_save_path}/training_summary.json", 'w') as f:
        json.dump(training_summary, f, indent=2)
    
    logger.info("🎉 BERT training completed successfully!")
    return model, tokenizer, training_summary

def test_trained_model(model, tokenizer):
    """Test the trained model with sample events"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.eval()
    
    test_events = [
        "coffee break with team",
        "weekly team meeting",
        "important client presentation", 
        "urgent project deadline",
        "EMERGENCY CEO meeting"
    ]
    
    logger.info("🧪 Testing trained model:")
    
    for event in test_events:
        encoding = tokenizer(
            event,
            truncation=True,
            padding='max_length',
            max_length=128,
            return_tensors='pt'
        ).to(device)
        
        with torch.no_grad():
            outputs = model(input_ids=encoding['input_ids'], 
                          attention_mask=encoding['attention_mask'])
            prediction = torch.argmax(outputs, dim=1).item() + 1  # Convert to 1-5 scale
            confidence = torch.softmax(outputs, dim=1).max().item()
        
        logger.info(f"  '{event}' → Priority {prediction} (confidence: {confidence:.3f})")

if __name__ == "__main__":
    logger.info("🚀 KairoCal BERT Priority Classifier Training Pipeline")
    logger.info("=" * 70)
    
    # Set random seeds for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)
    
    try:
        # Train the model
        model, tokenizer, summary = train_bert_model()
        
        # Test the trained model
        test_trained_model(model, tokenizer)
        
        logger.info("✅ Training pipeline completed successfully!")
        logger.info(f"📊 Final validation accuracy: {summary['final_val_accuracy']:.4f}")
        
    except Exception as e:
        logger.error(f"❌ Training failed: {str(e)}")
        raise
