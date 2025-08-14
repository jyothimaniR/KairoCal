#!/usr/bin/env python3
"""
RIGOROUS VERIFICATION AUDIT
Expose the truth about BERT training - no fake results allowed!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch
import torch.nn as nn
from transformers import DistilBertTokenizer, DistilBertModel
import json
import logging
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleBERTClassifier(nn.Module):
    """Simplified BERT classifier"""
    
    def __init__(self, num_classes=5, dropout=0.3):
        super().__init__()
        self.bert = DistilBertModel.from_pretrained('distilbert-base-uncased')
        
        self.classifier = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, num_classes)
        )
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]
        return self.classifier(cls_output)

def rigorous_verification_audit():
    """Comprehensive audit to expose the truth"""
    
    print("🔍 RIGOROUS VERIFICATION AUDIT - EXPOSE THE TRUTH!")
    print("=" * 60)
    print(f"⏰ Audit Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. CHECK FILE TIMESTAMPS
    print("📁 FILE TIMESTAMP ANALYSIS")
    print("-" * 40)
    
    model_path = "models/bert_priority_classifier"
    checkpoint_file = os.path.join(model_path, "pytorch_model.bin")
    metadata_file = os.path.join(model_path, "training_metadata.json")
    
    if os.path.exists(checkpoint_file):
        checkpoint_mtime = os.path.getmtime(checkpoint_file)
        checkpoint_time = datetime.fromtimestamp(checkpoint_mtime)
        print(f"✅ pytorch_model.bin last modified: {checkpoint_time}")
        
        # Check if modified today
        today = datetime.now().date()
        if checkpoint_time.date() == today:
            print("✅ Model file WAS modified today")
        else:
            print("❌ Model file was NOT modified today - suspicious!")
    
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        training_date = metadata.get("training_date", "unknown")
        accuracy = metadata.get("evaluation_metrics", {}).get("accuracy", 0)
        print(f"📊 Metadata training date: {training_date}")
        print(f"📊 Metadata accuracy: {accuracy:.1%}")
        
        # Check if this is old metadata
        if "2025-07-31" in training_date:
            print("🚨 SMOKING GUN: Metadata is from July 31st - OLD TRAINING!")
            print("❌ This proves the model wasn't actually retrained!")
        elif accuracy < 0.5:
            print("🚨 SMOKING GUN: Metadata shows poor accuracy - OLD MODEL!")
    
    print()
    
    # 2. MODEL WEIGHT ANALYSIS
    print("🧮 MODEL WEIGHT ANALYSIS")
    print("-" * 40)
    
    try:
        device = torch.device('cpu')
        checkpoint = torch.load(checkpoint_file, map_location=device, weights_only=False)
        
        # Check if model state exists
        if 'model_state_dict' in checkpoint:
            model_state = checkpoint['model_state_dict']
            
            # Calculate hash of model weights (to detect if it's actually different)
            weight_str = str(sorted([(k, v.sum().item()) for k, v in model_state.items()]))
            weight_hash = hashlib.md5(weight_str.encode()).hexdigest()[:8]
            print(f"🔢 Model weight hash: {weight_hash}")
            
            # Check specific layer weights
            classifier_weight = model_state.get('classifier.0.weight')
            if classifier_weight is not None:
                weight_mean = classifier_weight.mean().item()
                weight_std = classifier_weight.std().item()
                print(f"🎯 Classifier layer - Mean: {weight_mean:.6f}, Std: {weight_std:.6f}")
                
                # Random weights typically have mean near 0 and std around 0.02-0.1
                if abs(weight_mean) < 0.001 and 0.01 < weight_std < 0.2:
                    print("⚠️  Weights look randomly initialized - possibly untrained!")
                elif abs(weight_mean) > 0.01 or weight_std > 0.5:
                    print("✅ Weights show training patterns")
                else:
                    print("❓ Weight pattern unclear")
        else:
            print("❌ No model_state_dict found in checkpoint!")
            
    except Exception as e:
        print(f"❌ Failed to analyze model weights: {e}")
    
    print()
    
    # 3. COMPLETELY NEW TEST CASES (never seen in training)
    print("🧪 BRAND NEW TEST CASES - NEVER SEEN BEFORE")
    print("-" * 50)
    
    # These are completely new examples, different from anything in training
    brand_new_test_cases = [
        {
            "title": "System maintenance scheduled for weekend",
            "description": "Routine server maintenance and updates planned for Saturday",
            "expected_priority_range": [2, 3],  # Should be low-medium
            "reasoning": "Scheduled maintenance is routine"
        },
        {
            "title": "Fire drill evacuation exercise",
            "description": "Mandatory fire safety drill for all building occupants",
            "expected_priority_range": [3, 4],  # Should be medium-high
            "reasoning": "Safety drill is important but planned"
        },
        {
            "title": "Database corruption detected",
            "description": "Primary database showing signs of data corruption, investigating",
            "expected_priority_range": [4, 5],  # Should be high-critical
            "reasoning": "Database issues are critical"
        },
        {
            "title": "Office holiday party planning",
            "description": "Organizing December holiday celebration for staff",
            "expected_priority_range": [1, 2],  # Should be very low-low
            "reasoning": "Social event planning is low priority"
        },
        {
            "title": "Competitor analysis research",
            "description": "Market research on competing products and services",
            "expected_priority_range": [2, 3],  # Should be low-medium
            "reasoning": "Research is important but not urgent"
        }
    ]
    
    try:
        # Load model
        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        model = SimpleBERTClassifier(num_classes=5, dropout=0.3)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        
        priority_labels = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
        
        correct_predictions = 0
        total_predictions = len(brand_new_test_cases)
        
        print("Results:")
        for i, test in enumerate(brand_new_test_cases, 1):
            text = f"{test['title']}. {test['description']}".strip()
            
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
            
            with torch.no_grad():
                outputs = model(inputs['input_ids'], inputs['attention_mask'])
                probabilities = torch.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = torch.max(probabilities).item()
            
            priority = predicted_class + 1
            is_correct = priority in test['expected_priority_range']
            if is_correct:
                correct_predictions += 1
            
            status = "✅" if is_correct else "❌"
            print(f"{status} Test {i}: '{test['title']}'")
            print(f"     Predicted: Priority {priority} ({priority_labels[priority]}) - {confidence:.1%} confidence")
            print(f"     Expected: Priority {test['expected_priority_range']} - {test['reasoning']}")
            print()
        
        accuracy_rate = correct_predictions / total_predictions * 100
        print(f"🎯 Brand New Test Accuracy: {correct_predictions}/{total_predictions} ({accuracy_rate:.1f}%)")
        
        if accuracy_rate >= 80:
            print("✅ Model shows good generalization on new examples")
        elif accuracy_rate >= 60:
            print("⚠️  Model shows moderate performance on new examples")
        else:
            print("❌ Model performs poorly on new examples - likely overfitted or undertrained")
            
    except Exception as e:
        print(f"❌ Failed to test model on new cases: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # 4. EDGE CASE AND CONFUSING EXAMPLES
    print("🌪️  EDGE CASES AND CONFUSING EXAMPLES")
    print("-" * 40)
    
    edge_cases = [
        {
            "title": "Urgent lunch meeting",
            "description": "Lunch meeting with important client",
            "note": "Tests if 'urgent' + 'lunch' confuses the model"
        },
        {
            "title": "Critical coffee supplies running low",
            "description": "Office coffee machine needs restocking",
            "note": "Tests if 'critical' + trivial task confuses model"
        },
        {
            "title": "Regular emergency drill",
            "description": "Monthly scheduled emergency evacuation practice",
            "note": "Tests contradiction: 'regular' vs 'emergency'"
        },
        {
            "title": "Low priority system failure",
            "description": "Minor system component not working properly",
            "note": "Tests contradiction: 'low priority' vs 'system failure'"
        },
        {
            "title": "Meeting",
            "description": "",
            "note": "Tests minimal information"
        }
    ]
    
    try:
        print("Edge case results:")
        for i, test in enumerate(edge_cases, 1):
            text = f"{test['title']}. {test['description']}".strip()
            
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
            
            with torch.no_grad():
                outputs = model(inputs['input_ids'], inputs['attention_mask'])
                probabilities = torch.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = torch.max(probabilities).item()
            
            priority = predicted_class + 1
            
            print(f"🌪️  Edge Case {i}: '{test['title']}'")
            print(f"     Result: Priority {priority} ({priority_labels[priority]}) - {confidence:.1%} confidence")
            print(f"     Note: {test['note']}")
            print()
            
    except Exception as e:
        print(f"❌ Failed to test edge cases: {e}")
    
    print()
    
    # 5. FINAL VERDICT
    print("⚖️  FINAL AUDIT VERDICT")
    print("=" * 30)
    
    # Check if we found evidence of fake results
    suspicious_indicators = []
    
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        if metadata.get("evaluation_metrics", {}).get("accuracy", 0) < 0.5:
            suspicious_indicators.append("Metadata shows old poor accuracy")
        if "2025-07-31" in metadata.get("training_date", ""):
            suspicious_indicators.append("Training date is from July 31st, not recent")
    
    if suspicious_indicators:
        print("🚨 AUDIT CONCLUSION: TRAINING WAS NOT SUCCESSFUL!")
        print("❌ EVIDENCE OF FAKE/OLD RESULTS:")
        for indicator in suspicious_indicators:
            print(f"   • {indicator}")
        print()
        print("💡 RECOMMENDATION: Re-run the training script properly and verify results")
        return False
    else:
        print("✅ AUDIT CONCLUSION: Training appears legitimate")
        return True

if __name__ == "__main__":
    success = rigorous_verification_audit()
    
    print("\n" + "🔍" * 50)
    if success:
        print("✅ AUDIT PASSED: Results appear legitimate")
    else:
        print("❌ AUDIT FAILED: Evidence of fake/incomplete training!")
        print("🔄 NEED TO RE-RUN TRAINING PROPERLY!")
    print("🔍" * 50)
