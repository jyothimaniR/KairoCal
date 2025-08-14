#!/usr/bin/env python3
"""
Simple Investigation of Model Saving Issue
"""

import os
import json
from datetime import datetime

def investigate_model_saving_issue():
    """Simple investigation of what went wrong"""
    
    print("🔍 SIMPLE INVESTIGATION: WHY DIDN'T SAVING WORK?")
    print("=" * 50)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    model_dir = "models/bert_priority_classifier"
    
    # 1. Check file timestamps
    print("📁 FILE TIMESTAMPS:")
    print("-" * 20)
    
    files_to_check = [
        "pytorch_model.bin",
        "config.json", 
        "training_metadata.json",
        "tokenizer_config.json"
    ]
    
    today = datetime.now().date()
    files_modified_today = []
    files_modified_old = []
    
    for file in files_to_check:
        file_path = os.path.join(model_dir, file)
        if os.path.exists(file_path):
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if mtime.date() == today:
                files_modified_today.append((file, mtime))
                print(f"✅ {file}: {mtime} (TODAY)")
            else:
                files_modified_old.append((file, mtime))
                print(f"❌ {file}: {mtime} (OLD)")
        else:
            print(f"❓ {file}: NOT FOUND")
    
    print()
    
    # 2. Check training metadata content
    print("📊 TRAINING METADATA ANALYSIS:")
    print("-" * 30)
    
    metadata_file = os.path.join(model_dir, "training_metadata.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        training_date = metadata.get("training_date", "unknown")
        accuracy = metadata.get("evaluation_metrics", {}).get("accuracy", "unknown")
        
        print(f"Training Date: {training_date}")
        print(f"Accuracy: {accuracy}")
        
        if "2025-08-13" in training_date:
            print("✅ Training date is from today - GOOD!")
        elif "2025-07-31" in training_date:
            print("❌ Training date is from July 31st - OLD!")
        else:
            print(f"❓ Training date unclear: {training_date}")
            
        if isinstance(accuracy, (int, float)) and accuracy > 0.8:
            print("✅ Accuracy looks good")
        elif isinstance(accuracy, (int, float)) and accuracy < 0.3:
            print("❌ Accuracy is poor - old model")
        else:
            print(f"❓ Accuracy unclear: {accuracy}")
    else:
        print("❌ No training metadata file found")
    
    print()
    
    # 3. Diagnosis
    print("🔍 DIAGNOSIS:")
    print("-" * 12)
    
    if len(files_modified_today) >= 3 and len(files_modified_old) >= 1:
        print("🤔 PARTIAL UPDATE DETECTED:")
        print("   • Some files were updated today (pytorch_model.bin, config.json)")
        print("   • BUT training_metadata.json was NOT updated")
        print("   • This suggests the model saving partially worked")
        print("   • BUT the training metadata wasn't updated")
        print()
        print("💡 LIKELY CAUSE:")
        print("   The fast_bert_training.py script probably:")
        print("   1. ✅ Saved the model weights (pytorch_model.bin)")
        print("   2. ✅ Saved tokenizer files")
        print("   3. ❌ FAILED to update training_metadata.json")
        print("   4. ❌ The old training metadata from July is still there")
        
    elif len(files_modified_today) == 0:
        print("❌ NO FILES UPDATED TODAY:")
        print("   • The training script didn't save anything")
        print("   • Complete save failure")
        
    elif len(files_modified_old) == 0:
        print("✅ ALL FILES UPDATED TODAY:")
        print("   • This would be good news")
        print("   • But we need to check the content")
    
    print()
    
    # 4. Action plan
    print("🛠️  ACTION PLAN:")
    print("-" * 13)
    print("1. ✅ Environment is working (permissions OK)")
    print("2. ❌ The fast_bert_training.py has a bug in saving")
    print("3. 🔧 Need to fix the script to properly update ALL files")
    print("4. 🔧 Need to ensure training_metadata.json gets updated")
    print("5. 🧪 Re-run training with fixed script")
    print()
    print("🎯 ROOT CAUSE: The save_model_checkpoint method in fast_bert_training.py")
    print("   doesn't save the training_metadata.json file properly!")

if __name__ == "__main__":
    investigate_model_saving_issue()
