#!/usr/bin/env python3
"""
Quick BERT Model Status Check
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier

def main():
    print("🔍 BERT Model Status Check")
    print("=" * 50)
    
    try:
        # Load the classifier
        model_path = "models/bert_priority_classifier"
        classifier = AdvancedEventPriorityClassifier(model_path=model_path)
        
        print(f"📂 Model Path: {model_path}")
        print(f"🤖 Model Loaded: {classifier.bert_model is not None}")
        print(f"🔧 Feature Combiner: {classifier.feature_combiner is not None}")
        print(f"✅ Is Trained: {classifier.is_trained}")
        
        # Check if file exists
        checkpoint_path = os.path.join(model_path, 'pytorch_model.bin')
        print(f"📁 Checkpoint exists: {os.path.exists(checkpoint_path)}")
        
        # Try to load checkpoint directly
        if os.path.exists(checkpoint_path):
            import torch
            checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
            print(f"📊 Checkpoint keys: {list(checkpoint.keys())}")
            print(f"🏷️ Is Trained in checkpoint: {checkpoint.get('is_trained', 'NOT FOUND')}")
            print(f"🤖 BERT model in checkpoint: {'bert_model' in checkpoint}")
            print(f"🔧 Feature combiner in checkpoint: {'feature_combiner' in checkpoint}")
        
        # Test a simple prediction
        test_event = {
            "title": "Test event",
            "description": "This is a test",
            "start_time": "2025-08-01T10:00:00",
            "location": "Test location"
        }
        
        print(f"\n🧪 Testing prediction...")
        priority, confidence = classifier.predict(test_event)
        print(f"📊 Result: Priority {priority}, Confidence {confidence:.3f}")
        
        if classifier.is_trained:
            print("\n✅ BERT model is properly loaded and marked as trained!")
        else:
            print("\n❌ BERT model is not marked as trained!")
            print("🔍 This means predictions are using the fallback system")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
