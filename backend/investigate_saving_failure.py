#!/usr/bin/env python3
"""
INVESTIGATE SAVING FAILURE
Debug why the model saving didn't work
"""

import os
import sys
import torch
import json
from datetime import datetime
from transformers import DistilBertTokenizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_file_permissions():
    """Test file permissions and access to model directory"""
    
    logger.info("🔍 INVESTIGATING FILE PERMISSIONS AND SAVING")
    logger.info("=" * 50)
    
    model_dir = "models/bert_priority_classifier"
    
    # Check if directory exists
    if os.path.exists(model_dir):
        logger.info(f"✅ Directory exists: {model_dir}")
    else:
        logger.info(f"❌ Directory does not exist: {model_dir}")
        return False
    
    # Check write permissions
    test_file = os.path.join(model_dir, "test_write.tmp")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        logger.info("✅ Write permissions OK")
    except Exception as e:
        logger.error(f"❌ Write permission error: {e}")
        return False
    
    # Check existing files
    logger.info("\n📁 EXISTING FILES:")
    for file in os.listdir(model_dir):
        file_path = os.path.join(model_dir, file)
        size = os.path.getsize(file_path)
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        logger.info(f"   {file}: {size:,} bytes, modified {mtime}")
    
    return True

def test_pytorch_save():
    """Test if PyTorch save operation works"""
    
    logger.info("\n🔧 TESTING PYTORCH SAVE OPERATION")
    logger.info("-" * 40)
    
    try:
        # Create a simple model state dict
        test_model_state = {
            'test_layer.weight': torch.randn(10, 5),
            'test_layer.bias': torch.randn(10)
        }
        
        test_checkpoint = {
            'model_state_dict': test_model_state,
            'test_metadata': {
                'created_at': datetime.now().isoformat(),
                'test_run': True
            }
        }
        
        # Try to save
        test_path = "models/bert_priority_classifier/test_checkpoint.bin"
        torch.save(test_checkpoint, test_path)
        logger.info(f"✅ PyTorch save successful: {test_path}")
        
        # Try to load back
        loaded = torch.load(test_path, map_location='cpu', weights_only=False)
        logger.info(f"✅ PyTorch load successful: {loaded['test_metadata']}")
        
        # Clean up
        os.remove(test_path)
        return True
        
    except Exception as e:
        logger.error(f"❌ PyTorch save/load failed: {e}")
        return False

def test_tokenizer_save():
    """Test if tokenizer save works"""
    
    logger.info("\n🤖 TESTING TOKENIZER SAVE OPERATION")
    logger.info("-" * 40)
    
    try:
        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        
        test_dir = "models/bert_priority_classifier/test_tokenizer"
        os.makedirs(test_dir, exist_ok=True)
        
        tokenizer.save_pretrained(test_dir)
        logger.info(f"✅ Tokenizer save successful: {test_dir}")
        
        # Clean up
        import shutil
        shutil.rmtree(test_dir)
        return True
        
    except Exception as e:
        logger.error(f"❌ Tokenizer save failed: {e}")
        return False

def analyze_fast_training_script():
    """Analyze the fast_bert_training.py script for issues"""
    
    logger.info("\n📋 ANALYZING FAST_BERT_TRAINING.PY SCRIPT")
    logger.info("-" * 45)
    
    script_path = "fast_bert_training.py"
    if not os.path.exists(script_path):
        logger.error(f"❌ Script not found: {script_path}")
        return False
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Check for key components
    checks = [
        ("save_model_checkpoint method", "def save_model_checkpoint"),
        ("torch.save call", "torch.save"),
        ("tokenizer.save_pretrained", "tokenizer.save_pretrained"),
        ("Training metadata", "training_metadata"),
        ("Model state dict", "model_state_dict"),
        ("Config save", "config.json")
    ]
    
    for check_name, pattern in checks:
        if pattern in content:
            logger.info(f"✅ {check_name}: Found")
        else:
            logger.error(f"❌ {check_name}: Missing")
    
    # Look for potential issues
    issues = []
    
    if "except" not in content or "try:" not in content:
        issues.append("No error handling in save operations")
    
    if "logger.error" not in content:
        issues.append("No error logging for debugging")
    
    if issues:
        logger.warning("⚠️  POTENTIAL ISSUES:")
        for issue in issues:
            logger.warning(f"   • {issue}")
    else:
        logger.info("✅ Script structure looks good")
    
    return True

def check_previous_training_logs():
    """Check if there are any previous training logs or outputs"""
    
    logger.info("\n📜 CHECKING FOR PREVIOUS TRAINING EVIDENCE")
    logger.info("-" * 42)
    
    # Check if there are any log files or output files
    possible_log_files = [
        "training.log",
        "bert_training.log",
        "fast_training.log"
    ]
    
    log_files_found = []
    for log_file in possible_log_files:
        if os.path.exists(log_file):
            log_files_found.append(log_file)
    
    if log_files_found:
        logger.info(f"📄 Found log files: {log_files_found}")
        for log_file in log_files_found:
            logger.info(f"   Last modified: {datetime.fromtimestamp(os.path.getmtime(log_file))}")
    else:
        logger.info("📄 No dedicated log files found")
    
    # Check the old training metadata
    metadata_file = "models/bert_priority_classifier/training_metadata.json"
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        logger.info("📊 OLD TRAINING METADATA:")
        logger.info(f"   Date: {metadata.get('training_date', 'Unknown')}")
        logger.info(f"   Accuracy: {metadata.get('evaluation_metrics', {}).get('accuracy', 'Unknown')}")
        logger.info(f"   Duration: {metadata.get('training_duration_minutes', 'Unknown')} minutes")
    
    return True

def main():
    """Run all diagnostic tests"""
    
    print("🔍 BERT TRAINING SAVE FAILURE INVESTIGATION")
    print("=" * 55)
    print(f"⏰ Investigation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    
    # Run tests
    results.append(("File Permissions", test_file_permissions()))
    results.append(("PyTorch Save/Load", test_pytorch_save()))
    results.append(("Tokenizer Save", test_tokenizer_save()))
    results.append(("Script Analysis", analyze_fast_training_script()))
    results.append(("Previous Training Evidence", check_previous_training_logs()))
    
    # Summary
    print("\n" + "=" * 55)
    print("🔍 INVESTIGATION SUMMARY")
    print("=" * 55)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ CONCLUSION: Environment and permissions are OK")
        print("💡 The issue is likely in the training script logic or execution")
    else:
        print("❌ CONCLUSION: Found environmental issues that need fixing")
    
    print("\n🔧 NEXT STEPS:")
    print("1. Fix any environmental issues found")
    print("2. Add better error handling to training script")
    print("3. Add debug logging to save operations")
    print("4. Re-run training with verbose logging")

if __name__ == "__main__":
    main()
