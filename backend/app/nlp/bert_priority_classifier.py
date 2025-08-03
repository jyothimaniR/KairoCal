# backend/app/nlp/bert_priority_classifier.py
"""
Advanced BERT-based Event Priority Classification System
Replaces keyword-based priority inference with intelligent contextual understanding
"""

import torch
import torch.nn as nn
import numpy as np
from transformers import (
    DistilBertTokenizer, 
    DistilBertModel, 
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)
from typing import Dict, Any, Tuple, List, Optional
import json
import logging
import os
from datetime import datetime, timedelta
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

class AdvancedEventPriorityClassifier:
    """
    Advanced BERT-based priority classifier with multi-dimensional features
    
    Features:
    - DistilBERT for semantic understanding
    - Temporal context encoding
    - User behavior patterns
    - Location context
    - Confidence scoring
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        
        # Feature scalers (initialize defaults)
        self.temporal_scaler = StandardScaler()
        self.location_encoder = {}
        self.is_trained = False
        
        # Initialize models
        if model_path and os.path.exists(model_path):
            self._load_trained_model(model_path)
        else:
            self._initialize_new_model()
        
        # Priority categories for interpretability
        self.priority_labels = {
            1: "Very Low",
            2: "Low", 
            3: "Medium",
            4: "High",
            5: "Critical"
        }
        
    def _initialize_new_model(self):
        """Initialize a new untrained model"""
        self.bert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')
        
        # Custom classifier head combining BERT + features
        self.feature_combiner = nn.Sequential(
            nn.Linear(768 + 64, 256),  # BERT embeddings + feature vector
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(), 
            nn.Dropout(0.2),
            nn.Linear(128, 5)  # 5 priority classes
        )
        
        self.bert_model.to(self.device)
        self.feature_combiner.to(self.device)
        
    def _load_trained_model(self, model_path: str):
        """Load a pre-trained model"""
        checkpoint_path = os.path.join(model_path, 'pytorch_model.bin')
        
        if os.path.exists(checkpoint_path):
            checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
            
            # Initialize models first
            self.bert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')
            self.feature_combiner = nn.Sequential(
                nn.Linear(768 + 64, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, 5)
            )
            
            # Load state dicts
            if checkpoint['bert_model']:
                self.bert_model.load_state_dict(checkpoint['bert_model'])
            if checkpoint['feature_combiner']:
                self.feature_combiner.load_state_dict(checkpoint['feature_combiner'])
                
            self.temporal_scaler = checkpoint.get('temporal_scaler')
            self.location_encoder = checkpoint.get('location_encoder')
            self.is_trained = checkpoint.get('is_trained', True)  # Default to True if model exists
            
            # Move to device
            self.bert_model.to(self.device)
            self.feature_combiner.to(self.device)
            
            logger.info(f"Loaded trained model from {model_path}")
            
            # If we successfully loaded model components, mark as trained
            if self.bert_model and self.feature_combiner:
                self.is_trained = True
        else:
            logger.warning(f"No saved model found at {model_path}")
            self.is_trained = False
        
    def save_model(self, model_path: str):
        """Save the trained model"""
        # Ensure the directory exists
        os.makedirs(model_path, exist_ok=True)
        
        # Save model components
        checkpoint_path = os.path.join(model_path, 'pytorch_model.bin')
        checkpoint = {
            'bert_model': self.bert_model.state_dict() if self.bert_model else None,
            'feature_combiner': self.feature_combiner.state_dict() if self.feature_combiner else None,
            'temporal_scaler': self.temporal_scaler,
            'location_encoder': self.location_encoder,
            'is_trained': self.is_trained
        }
        torch.save(checkpoint, checkpoint_path)
        
        # Save config
        config_path = os.path.join(model_path, 'config.json')
        config = {
            'model_type': 'AdvancedEventPriorityClassifier',
            'bert_model_name': 'distilbert-base-uncased',
            'num_classes': 5,
            'created_at': datetime.now().isoformat()
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Save tokenizer
        if self.tokenizer:
            self.tokenizer.save_pretrained(model_path)
        
        logger.info(f"Model saved to {model_path}")
        
    def _extract_text_features(self, text: str) -> torch.Tensor:
        """Extract BERT embeddings from event text"""
        # Tokenize and encode
        inputs = self.tokenizer(
            text, 
            return_tensors='pt',
            truncation=True,
            padding=True,
            max_length=128
        ).to(self.device)
        
        # Get BERT embeddings
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
            # Use [CLS] token embedding
            embeddings = outputs.last_hidden_state[:, 0, :]  # Shape: (1, 768)
            
        return embeddings
        
    def _extract_temporal_features(self, event_data: Dict[str, Any]) -> np.ndarray:
        """Extract temporal context features"""
        features = []
        
        try:
            start_time = event_data.get('start_time')
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time)
            elif not isinstance(start_time, datetime):
                start_time = datetime.now()
                
            # Time of day (0-23)
            hour = start_time.hour
            features.extend([
                np.sin(2 * np.pi * hour / 24),  # Cyclical encoding
                np.cos(2 * np.pi * hour / 24)
            ])
            
            # Day of week (0-6)
            day_of_week = start_time.weekday()
            features.extend([
                np.sin(2 * np.pi * day_of_week / 7),
                np.cos(2 * np.pi * day_of_week / 7)
            ])
            
            # Time until event (urgency)
            time_until = (start_time - datetime.now()).total_seconds() / 3600  # hours
            features.append(min(time_until / 168, 1.0))  # Normalize to weekly scale
            
            # Duration
            end_time = event_data.get('end_time')
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time)
            elif not isinstance(end_time, datetime):
                end_time = start_time + timedelta(hours=1)
                
            duration = (end_time - start_time).total_seconds() / 3600  # hours
            features.append(min(duration / 8, 1.0))  # Normalize to 8-hour scale
            
            # Is weekend
            features.append(1.0 if day_of_week >= 5 else 0.0)
            
            # Business hours (9-17)
            features.append(1.0 if 9 <= hour <= 17 else 0.0)
            
        except Exception as e:
            logger.warning(f"Error extracting temporal features: {e}")
            features = [0.0] * 8
            
        return np.array(features)
        
    def _extract_location_features(self, location: Optional[str]) -> np.ndarray:
        """Extract location-based features"""
        features = []
        
        if not location:
            return np.zeros(8)
            
        location_lower = location.lower()
        
        # Location type indicators
        location_types = {
            'office': ['office', 'building', 'workplace', 'work'],
            'home': ['home', 'house', 'apartment'],
            'meeting_room': ['room', 'conference', 'meeting'],
            'restaurant': ['restaurant', 'cafe', 'lunch', 'dinner'],
            'medical': ['hospital', 'clinic', 'doctor', 'medical'],
            'gym': ['gym', 'fitness', 'workout'],
            'outdoor': ['park', 'outdoor', 'field', 'beach'],
            'remote': ['zoom', 'teams', 'virtual', 'online', 'remote']
        }
        
        for location_type, keywords in location_types.items():
            features.append(1.0 if any(keyword in location_lower for keyword in keywords) else 0.0)
            
        return np.array(features)
        
    def _extract_content_features(self, event_data: Dict[str, Any]) -> np.ndarray:
        """Extract content-based features beyond BERT"""
        features = []
        
        title = event_data.get('title', '').lower()
        description = event_data.get('description', '').lower()
        text = f"{title} {description}"
        
        # Text length indicators
        features.append(min(len(text) / 100, 1.0))  # Normalized text length
        
        # Urgency indicators
        urgency_words = ['urgent', 'asap', 'immediate', 'emergency', 'critical']
        features.append(1.0 if any(word in text for word in urgency_words) else 0.0)
        
        # Formality indicators
        formal_words = ['meeting', 'presentation', 'conference', 'interview']
        features.append(1.0 if any(word in text for word in formal_words) else 0.0)
        
        # Personal indicators
        personal_words = ['personal', 'family', 'hobby', 'leisure', 'vacation']
        features.append(1.0 if any(word in text for word in personal_words) else 0.0)
        
        # Work indicators
        work_words = ['project', 'deadline', 'client', 'team', 'work']
        features.append(1.0 if any(word in text for word in work_words) else 0.0)
        
        # Health indicators
        health_words = ['doctor', 'appointment', 'medical', 'health']
        features.append(1.0 if any(word in text for word in health_words) else 0.0)
        
        # Social indicators
        social_words = ['lunch', 'dinner', 'party', 'social', 'friends']
        features.append(1.0 if any(word in text for word in social_words) else 0.0)
        
        # Executive/VIP indicators
        vip_words = ['ceo', 'director', 'manager', 'executive', 'boss']
        features.append(1.0 if any(word in text for word in vip_words) else 0.0)
        
        return np.array(features)
        
    def _combine_features(self, event_data: Dict[str, Any], user_context: Optional[Dict] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """Combine all features for classification"""
        # Text features (BERT)
        title = event_data.get('title', '')
        description = event_data.get('description', '')
        text = f"{title}. {description}".strip()
        text_features = self._extract_text_features(text)
        
        # Other features
        temporal_features = self._extract_temporal_features(event_data)
        location_features = self._extract_location_features(event_data.get('location'))
        content_features = self._extract_content_features(event_data)
        
        # User context features (placeholder for future enhancement)
        user_features = np.zeros(8)
        if user_context:
            # TODO: Integrate with UserBehaviorAnalyzer
            pass
            
        # Combine all non-text features
        combined_features = np.concatenate([
            temporal_features,    # 8 features
            location_features,    # 8 features  
            content_features,     # 8 features
            user_features         # 8 features
        ])  # Total: 32 features
        
        # Pad to 64 features for consistent input size
        if len(combined_features) < 64:
            combined_features = np.pad(combined_features, (0, 64 - len(combined_features)))
        else:
            combined_features = combined_features[:64]
            
        feature_tensor = torch.FloatTensor(combined_features).unsqueeze(0).to(self.device)
        
        return text_features, feature_tensor
        
    def predict(self, event_data: Dict[str, Any], user_context: Optional[Dict] = None) -> Tuple[int, float]:
        """
        Predict event priority with confidence score
        
        Args:
            event_data: Event information (title, description, start_time, etc.)
            user_context: User behavior context (optional)
            
        Returns:
            Tuple of (priority: int 1-5, confidence: float 0-1)
        """
        if not self.is_trained:
            logger.warning("Model not trained yet, falling back to rule-based classification")
            return self._fallback_priority_classification(event_data)
            
        try:
            self.bert_model.eval()
            self.feature_combiner.eval()
            
            with torch.no_grad():
                # Extract and combine features
                text_features, other_features = self._combine_features(event_data, user_context)
                
                # Combine BERT embeddings with other features
                combined_input = torch.cat([text_features, other_features], dim=1)
                
                # Get predictions
                logits = self.feature_combiner(combined_input)
                probabilities = torch.softmax(logits, dim=1)
                
                # Get prediction and confidence
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = torch.max(probabilities).item()
                
                # Convert to 1-5 priority scale
                priority = predicted_class + 1
                
                logger.info(f"BERT Priority: {priority} ({self.priority_labels[priority]}) - Confidence: {confidence:.3f}")
                
                return priority, confidence
                
        except Exception as e:
            logger.error(f"Error in BERT prediction: {e}")
            return self._fallback_priority_classification(event_data)
            
    def _fallback_priority_classification(self, event_data: Dict[str, Any]) -> Tuple[int, float]:
        """Fallback to rule-based classification if BERT fails"""
        title = (event_data.get('title') or '').lower()
        description = (event_data.get('description') or '').lower()
        text = f"{title} {description}"
        
        # Simplified keyword-based classification
        if any(word in text for word in ['urgent', 'critical', 'emergency', 'ceo']):
            return 5, 0.7
        elif any(word in text for word in ['important', 'presentation', 'client']):
            return 4, 0.6
        elif any(word in text for word in ['meeting', 'work', 'project']):
            return 3, 0.5
        elif any(word in text for word in ['lunch', 'personal', 'hobby']):
            return 2, 0.4
        else:
            return 3, 0.3  # Default medium priority
            
    def explain_prediction(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide explanation for the priority prediction"""
        priority, confidence = self.predict(event_data)
        
        return {
            'priority': priority,
            'priority_label': self.priority_labels[priority],
            'confidence': confidence,
            'reasoning': {
                'text_analysis': f"Event title and description analysis",
                'temporal_context': f"Time: {event_data.get('start_time', 'Not specified')}",
                'location_context': f"Location: {event_data.get('location', 'Not specified')}",
                'model_confidence': f"{confidence:.1%} confident in this classification"
            }
        }
    
    def train(self, X_train: List[str], y_train: List[int], X_val: List[str], y_val: List[int],
              epochs: int = 3, learning_rate: float = 2e-5, batch_size: int = 16) -> Dict[str, Any]:
        """
        Train the BERT priority classifier
        
        Args:
            X_train: Training text data (list of event descriptions)
            y_train: Training labels (list of priority levels 1-5)
            X_val: Validation text data
            y_val: Validation labels
            epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
            batch_size: Batch size for training
            
        Returns:
            Training history dictionary with loss and accuracy metrics
        """
        from torch.utils.data import DataLoader, TensorDataset
        import torch.optim as optim
        from sklearn.metrics import accuracy_score, classification_report
        
        logger.info(f"🎯 Training BERT classifier with {len(X_train)} training samples")
        
        # Prepare training data with combined features
        logger.info("Preparing training data with combined features...")
        train_combined_features = []
        val_combined_features = []
        
        # Process training data
        for text in X_train:
            # Create dummy event data for feature extraction
            dummy_event = {
                'title': text.split('.')[0] if '.' in text else text[:50],
                'description': text,
                'start_time': datetime.now().isoformat(),
                'location': None
            }
            text_features, other_features = self._combine_features(dummy_event)
            combined = torch.cat([text_features, other_features], dim=1)
            train_combined_features.append(combined)
        
        # Process validation data  
        for text in X_val:
            dummy_event = {
                'title': text.split('.')[0] if '.' in text else text[:50],
                'description': text,
                'start_time': datetime.now().isoformat(),
                'location': None
            }
            text_features, other_features = self._combine_features(dummy_event)
            combined = torch.cat([text_features, other_features], dim=1)
            val_combined_features.append(combined)
        
        # Stack into tensors
        train_features_tensor = torch.stack(train_combined_features).squeeze(1)
        val_features_tensor = torch.stack(val_combined_features).squeeze(1)
        
        # Convert labels to tensors (0-indexed for PyTorch)
        train_labels = torch.tensor([label - 1 for label in y_train], dtype=torch.long)
        val_labels = torch.tensor([label - 1 for label in y_val], dtype=torch.long)
        
        # Create datasets
        train_dataset = TensorDataset(train_features_tensor, train_labels)
        val_dataset = TensorDataset(val_features_tensor, val_labels)
        
        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        # Initialize model for training
        self.bert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.feature_combiner = nn.Sequential(
            nn.Linear(768 + 64, 256),  # BERT embeddings (768) + other features (64)
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 5)  # 5 priority classes
        )
        
        # Move to device
        self.bert_model.to(self.device)
        self.feature_combiner.to(self.device)
        
        # Optimizer and loss function
        optimizer = optim.AdamW(
            list(self.bert_model.parameters()) + list(self.feature_combiner.parameters()),
            lr=learning_rate
        )
        criterion = nn.CrossEntropyLoss()
        
        # Training history
        history = {
            'train_loss': [],
            'train_accuracy': [],
            'val_loss': [],
            'val_accuracy': []
        }
        
        # Training loop
        for epoch in range(epochs):
            logger.info(f"📚 Epoch {epoch + 1}/{epochs}")
            
            # Training phase
            self.bert_model.train()
            self.feature_combiner.train()
            train_loss = 0.0
            train_predictions = []
            train_targets = []
            
            for batch_idx, (combined_features, labels) in enumerate(train_loader):
                combined_features = combined_features.to(self.device)
                labels = labels.to(self.device)
                
                optimizer.zero_grad()
                
                # Forward pass through classifier
                logits = self.feature_combiner(combined_features)
                loss = criterion(logits, labels)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                predictions = torch.argmax(logits, dim=1)
                train_predictions.extend(predictions.cpu().numpy())
                train_targets.extend(labels.cpu().numpy())
                
                if batch_idx % 10 == 0:
                    logger.info(f"   Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.4f}")
            
            # Calculate training metrics
            train_loss /= len(train_loader)
            train_accuracy = accuracy_score(train_targets, train_predictions)
            
            # Validation phase
            self.feature_combiner.eval()
            val_loss = 0.0
            val_predictions = []
            val_targets = []
            
            with torch.no_grad():
                for combined_features, labels in val_loader:
                    combined_features = combined_features.to(self.device)
                    labels = labels.to(self.device)
                    
                    # Forward pass
                    logits = self.feature_combiner(combined_features)
                    loss = criterion(logits, labels)
                    
                    val_loss += loss.item()
                    predictions = torch.argmax(logits, dim=1)
                    val_predictions.extend(predictions.cpu().numpy())
                    val_targets.extend(labels.cpu().numpy())
            
            val_loss /= len(val_loader)
            val_accuracy = accuracy_score(val_targets, val_predictions)
            
            # Store metrics
            history['train_loss'].append(train_loss)
            history['train_accuracy'].append(train_accuracy)
            history['val_loss'].append(val_loss)
            history['val_accuracy'].append(val_accuracy)
            
            logger.info(f"   📈 Train Loss: {train_loss:.4f}, Train Acc: {train_accuracy:.4f}")
            logger.info(f"   📊 Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}")
        
        # Mark as trained
        self.is_trained = True
        
        # Final validation report
        val_report = classification_report(val_targets, val_predictions, target_names=[f"Priority {i+1}" for i in range(5)])
        logger.info(f"📋 Final Classification Report:\n{val_report}")
        
        return history