# backend/app/nlp/model_loader.py
"""
BERT Model Loading Utility
Handles loading, caching, and fallback for BERT priority classifier models
"""

import os
import json
import logging
import torch
from typing import Optional, Dict, Any
from functools import lru_cache
from datetime import datetime
from pathlib import Path

from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
from app.config import get_settings

logger = logging.getLogger(__name__)

class ModelLoadError(Exception):
    """Custom exception for model loading errors"""
    pass

def check_model_files_exist() -> bool:
    """Check if required model files exist"""
    model_dir = Path("backend/models/bert_priority_classifier")
    required_files = ["pytorch_model.bin", "config.json", "tokenizer.json"]
    
    if not model_dir.exists():
        return False
        
    for file_name in required_files:
        if not (model_dir / file_name).exists():
            return False
    
    return True

class BERTModelLoader:
    """
    Centralized BERT model loading and caching system
    
    Features:
    - Automatic model loading with fallback
    - Model caching to avoid repeated loading
    - Device detection and optimization
    - Error handling and logging
    - Model metadata validation
    """
    
    _instance = None
    _cached_model = None
    _model_metadata = None
    _last_load_time = None
    
    def __new__(cls):
        """Singleton pattern to ensure single model instance"""
        if cls._instance is None:
            cls._instance = super(BERTModelLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.settings = get_settings()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_path = self.settings.bert_model_path
        
    def _check_model_files_exist(self) -> bool:
        """Check if required model files exist"""
        required_files = [
            'pytorch_model.bin',  # or 'model.safetensors'
            'config.json',
            'training_metadata.json'
        ]
        
        for file_name in required_files:
            file_path = os.path.join(self.model_path, file_name)
            if not os.path.exists(file_path):
                logger.debug(f"Missing model file: {file_path}")
                return False
        return True
    
    def _load_model_metadata(self) -> Optional[Dict[str, Any]]:
        """Load model training metadata"""
        metadata_path = os.path.join(self.model_path, 'training_metadata.json')
        
        if not os.path.exists(metadata_path):
            logger.warning(f"Model metadata not found: {metadata_path}")
            return None
            
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            logger.info(f"📊 Model metadata loaded:")
            logger.info(f"   Training Date: {metadata.get('training_date', 'Unknown')}")
            logger.info(f"   Accuracy: {metadata.get('evaluation_metrics', {}).get('accuracy', 'Unknown')}")
            logger.info(f"   Device: {metadata.get('device', 'Unknown')}")
            
            return metadata
            
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load model metadata: {str(e)}")
            return None
    
    def _validate_model_compatibility(self, metadata: Dict[str, Any]) -> bool:
        """Validate model compatibility with current configuration"""
        if not metadata:
            return True  # Skip validation if no metadata
            
        model_config = metadata.get('model_config', {})
        
        # Check priority levels compatibility
        model_priority_levels = model_config.get('priority_levels', 5)
        if model_priority_levels != self.settings.priority_levels:
            logger.warning(f"Priority levels mismatch: model={model_priority_levels}, config={self.settings.priority_levels}")
            return False
            
        # Check if model is too old (optional)
        training_date_str = metadata.get('training_date')
        if training_date_str:
            try:
                training_date = datetime.fromisoformat(training_date_str.replace('Z', '+00:00'))
                days_old = (datetime.now() - training_date).days
                
                if days_old > 30:  # Model older than 30 days
                    logger.warning(f"Model is {days_old} days old, consider retraining")
                    
            except ValueError:
                logger.warning("Invalid training date format in metadata")
        
        return True
    
    def load_trained_model(self, force_reload: bool = False) -> AdvancedEventPriorityClassifier:
        """
        Load trained BERT model with comprehensive error handling
        
        Args:
            force_reload: Force reload even if model is cached
            
        Returns:
            AdvancedEventPriorityClassifier instance
            
        Raises:
            ModelLoadError: If model loading fails
        """
        # Return cached model if available and not forcing reload
        if not force_reload and self._cached_model is not None:
            logger.debug("Using cached BERT model")
            return self._cached_model
        
        logger.info(f"🤖 Loading BERT model from: {self.model_path}")
        
        try:
            # Check if model files exist
            if not self._check_model_files_exist():
                raise ModelLoadError(f"Required model files not found in: {self.model_path}")
            
            # Load metadata
            metadata = self._load_model_metadata()
            
            # Validate compatibility
            if metadata and not self._validate_model_compatibility(metadata):
                logger.warning("Model compatibility issues detected, but proceeding with loading")
            
            # Initialize classifier with model path
            classifier = AdvancedEventPriorityClassifier(model_path=self.model_path)
            
            # Verify model is trained
            if not classifier.is_trained:
                raise ModelLoadError("Model loaded but not in trained state")
            
            # Cache the model
            self._cached_model = classifier
            self._model_metadata = metadata
            self._last_load_time = datetime.now()
            
            logger.info("✅ BERT model loaded successfully!")
            logger.info(f"📱 Device: {classifier.device}")
            logger.info(f"🧠 Model State: {'Trained' if classifier.is_trained else 'Untrained'}")
            
            return classifier
            
        except Exception as e:
            error_msg = f"Failed to load BERT model: {str(e)}"
            logger.error(error_msg)
            raise ModelLoadError(error_msg) from e
    
    def load_model_with_fallback(self) -> AdvancedEventPriorityClassifier:
        """
        Load model with automatic fallback to untrained model
        
        Returns:
            AdvancedEventPriorityClassifier instance (trained or fallback)
        """
        try:
            # Try to load trained model
            return self.load_trained_model()
            
        except ModelLoadError as e:
            logger.warning(f"Failed to load trained model: {str(e)}")
            logger.info("🔄 Falling back to untrained BERT classifier")
            
            # Fallback to untrained model
            classifier = AdvancedEventPriorityClassifier()
            
            # Cache fallback model
            self._cached_model = classifier
            self._last_load_time = datetime.now()
            
            logger.info("⚠️ Using fallback BERT classifier (rule-based predictions)")
            return classifier
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about currently loaded model"""
        if self._cached_model is None:
            return {
                'loaded': False,
                'error': 'No model loaded'
            }
        
        info = {
            'loaded': True,
            'trained': self._cached_model.is_trained,
            'device': str(self._cached_model.device),
            'load_time': self._last_load_time.isoformat() if self._last_load_time else None,
            'model_path': self.model_path,
            'files_exist': self._check_model_files_exist()
        }
        
        if self._model_metadata:
            info['metadata'] = {
                'training_date': self._model_metadata.get('training_date'),
                'accuracy': self._model_metadata.get('evaluation_metrics', {}).get('accuracy'),
                'training_duration': self._model_metadata.get('training_duration_minutes'),
                'priority_levels': self._model_metadata.get('model_config', {}).get('priority_levels')
            }
        
        return info
    
    def reload_model(self) -> AdvancedEventPriorityClassifier:
        """Force reload the model (useful after retraining)"""
        logger.info("🔄 Force reloading BERT model...")
        
        # Clear cache
        self._cached_model = None
        self._model_metadata = None
        self._last_load_time = None
        
        # Load fresh model
        return self.load_model_with_fallback()
    
    def is_model_available(self) -> bool:
        """Check if trained model is available"""
        return self._check_model_files_exist()
    
    def clear_cache(self):
        """Clear cached model (useful for memory management)"""
        logger.info("🧹 Clearing model cache")
        self._cached_model = None
        self._model_metadata = None
        self._last_load_time = None

# Convenience functions for easy access
@lru_cache(maxsize=1)
def get_model_loader() -> BERTModelLoader:
    """Get singleton model loader instance"""
    return BERTModelLoader()

def load_bert_model(force_reload: bool = False) -> AdvancedEventPriorityClassifier:
    """
    Convenience function to load BERT model with fallback
    
    Args:
        force_reload: Force reload even if cached
    
    Returns:
        AdvancedEventPriorityClassifier instance
    """
    loader = get_model_loader()
    return loader.load_model_with_fallback()

def get_model_status() -> Dict[str, Any]:
    """Get current model status information"""
    loader = get_model_loader()
    return loader.get_model_info()

def is_trained_model_available() -> bool:
    """Check if a trained model is available"""
    loader = get_model_loader()
    return loader.is_model_available()

# Module-level model instance for global access
_global_model = None

def get_global_bert_model() -> AdvancedEventPriorityClassifier:
    """
    Get global BERT model instance (lazy loading)
    
    Returns:
        AdvancedEventPriorityClassifier instance
    """
    global _global_model
    
    if _global_model is None:
        _global_model = load_bert_model()
        logger.info("🌐 Global BERT model initialized")
    
    return _global_model

def refresh_global_model():
    """Refresh global model instance (useful after retraining)"""
    global _global_model
    _global_model = None
    logger.info("🔄 Global BERT model cache cleared")
