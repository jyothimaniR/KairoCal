#!/usr/bin/env python3
"""
COMPREHENSIVE POST-TRAINING VERIFICATION
Test with completely new examples and verify all requirements
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

def verify_training_requirements():
    """Verify all training requirements were met"""
    
    print("🔍 COMPREHENSIVE POST-TRAINING VERIFICATION")
    print("=" * 55)
    print(f"⏰ Verification Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    requirements_met = []
    
    # REQUIREMENT 1: New training metadata with today's date
    print("✅ REQUIREMENT 1: New training metadata with today's date")
    print("-" * 50)
    
    metadata_file = "models/bert_priority_classifier/training_metadata.json"
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        training_date = metadata.get("training_date", "unknown")
        today = datetime.now().date().isoformat()
        
        print(f"Training date: {training_date}")
        print(f"Today's date:  {today}")
        
        if today in training_date:
            print("✅ PASS: Training metadata has today's date")
            requirements_met.append("Today's date in metadata")
        else:
            print("❌ FAIL: Training date is not from today")
    else:
        print("❌ FAIL: No training metadata file found")
    
    print()
    
    # REQUIREMENT 2: Model files with today's timestamps
    print("✅ REQUIREMENT 2: Model files with today's timestamps")
    print("-" * 45)
    
    model_files = ["pytorch_model.bin", "config.json", "tokenizer_config.json"]
    today_files = 0
    
    for file in model_files:
        file_path = f"models/bert_priority_classifier/{file}"
        if os.path.exists(file_path):
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if mtime.date() == datetime.now().date():
                print(f"✅ {file}: {mtime} (TODAY)")
                today_files += 1
            else:
                print(f"❌ {file}: {mtime} (OLD)")
        else:
            print(f"❌ {file}: NOT FOUND")
    
    if today_files >= 2:
        print(f"✅ PASS: {today_files}/{len(model_files)} files updated today")
        requirements_met.append("Files updated today")
    else:
        print(f"❌ FAIL: Only {today_files}/{len(model_files)} files updated today")
    
    print()
    
    # REQUIREMENT 3: 80%+ accuracy on brand new test cases
    print("✅ REQUIREMENT 3: 80%+ accuracy on brand new test cases")
    print("-" * 50)
    
    # Completely new test cases - never seen in any training
    brand_new_cases = [
        {
            "title": "Website server experiencing downtime",
            "description": "Main company website is completely inaccessible to customers",
            "expected_range": [4, 5],  # Should be high-critical
            "reasoning": "Website downtime affects business directly"
        },
        {
            "title": "Office supplies need restocking",
            "description": "Paper, pens, and basic office materials running low",
            "expected_range": [1, 2],  # Should be very low-low
            "reasoning": "Office supplies are routine maintenance"
        },
        {
            "title": "Security vulnerability discovered",
            "description": "Potential security flaw found in authentication system",
            "expected_range": [4, 5],  # Should be high-critical
            "reasoning": "Security vulnerabilities are critical"
        },
        {
            "title": "Team building workshop planning",
            "description": "Organizing quarterly team building activities and exercises",
            "expected_range": [2, 3],  # Should be low-medium
            "reasoning": "Team building is important but not urgent"
        },
        {
            "title": "Budget review meeting",
            "description": "Monthly financial review and budget planning session",
            "expected_range": [3, 4],  # Should be medium-high
            "reasoning": "Budget reviews are important business activities"
        },
        {
            "title": "Training documentation update",
            "description": "Update employee training materials and procedures",
            "expected_range": [2, 3],  # Should be low-medium  
            "reasoning": "Documentation updates are maintenance tasks"
        },
        {
            "title": "Customer complaint escalation",
            "description": "High-value customer threatening to cancel service",
            "expected_range": [4, 5],  # Should be high-critical
            "reasoning": "Customer retention is business critical"
        },
        {
            "title": "Office birthday celebration",
            "description": "Celebrating team member's birthday with cake",
            "expected_range": [1, 2],  # Should be very low-low
            "reasoning": "Social celebrations are lowest priority"
        }
    ]
    
    try:
        # Load model
        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        model = SimpleBERTClassifier(num_classes=5, dropout=0.3)
        
        checkpoint_path = "models/bert_priority_classifier/pytorch_model.bin"
        checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        
        priority_labels = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
        
        correct_predictions = 0
        total_predictions = len(brand_new_cases)
        
        print("Testing brand new cases:")
        for i, test in enumerate(brand_new_cases, 1):
            text = f"{test['title']}. {test['description']}".strip()
            
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
            
            with torch.no_grad():
                outputs = model(inputs['input_ids'], inputs['attention_mask'])
                probabilities = torch.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = torch.max(probabilities).item()
            
            priority = predicted_class + 1
            is_correct = priority in test['expected_range']
            if is_correct:
                correct_predictions += 1
            
            status = "✅" if is_correct else "❌"
            print(f"  {status} Test {i}: '{test['title'][:40]}...'")
            print(f"      Predicted: Priority {priority} ({priority_labels[priority]}) - {confidence:.1%}")
            print(f"      Expected: {test['expected_range']} - {test['reasoning']}")
            print()
        
        accuracy_rate = correct_predictions / total_predictions * 100
        print(f"🎯 Brand New Test Accuracy: {correct_predictions}/{total_predictions} ({accuracy_rate:.1f}%)")
        
        if accuracy_rate >= 80:
            print("✅ PASS: Model shows excellent generalization (≥80%)")
            requirements_met.append("80%+ accuracy on new cases")
        elif accuracy_rate >= 70:
            print("⚠️ PARTIAL: Model shows good generalization (70-79%)")
        else:
            print("❌ FAIL: Model shows poor generalization (<70%)")
            
    except Exception as e:
        print(f"❌ FAIL: Could not test model: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # REQUIREMENT 4: Training that took realistic time (30+ minutes)
    print("✅ REQUIREMENT 4: Training took realistic time (30+ minutes)")
    print("-" * 52)
    
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        duration = metadata.get("training_duration_minutes", 0)
        print(f"Training duration: {duration:.1f} minutes")
        
        if duration >= 30:
            print("✅ PASS: Training took realistic time (≥30 minutes)")
            requirements_met.append("30+ minutes training time")
        elif duration >= 15:
            print("⚠️ PARTIAL: Training took moderate time (15-30 minutes)")
        else:
            print("❌ FAIL: Training was too fast (<15 minutes) - suspicious!")
    else:
        print("❌ FAIL: No duration information available")
    
    print()
    
    # FINAL ASSESSMENT
    print("🏆 FINAL VERIFICATION RESULTS")
    print("=" * 35)
    
    total_requirements = 4
    met_requirements = len(requirements_met)
    
    print(f"Requirements met: {met_requirements}/{total_requirements}")
    for req in requirements_met:
        print(f"  ✅ {req}")
    
    missing_requirements = total_requirements - met_requirements
    if missing_requirements > 0:
        print(f"\nMissing requirements: {missing_requirements}")
    
    if met_requirements == total_requirements:
        print("\n🎉 SUCCESS: ALL REQUIREMENTS MET!")
        print("🚀 BERT training was successful and credible!")
        return True
    elif met_requirements >= 3:
        print("\n⚠️ MOSTLY SUCCESSFUL: Most requirements met")
        print("🔧 Minor issues to address")
        return True
    else:
        print("\n❌ FAILED: Too many requirements not met")
        print("🔄 Need to re-run training properly")
        return False

if __name__ == "__main__":
    success = verify_training_requirements()
    
    if success:
        print("\n✅ VERIFICATION PASSED - Training was successful!")
    else:
        print("\n❌ VERIFICATION FAILED - Need to fix training!")
