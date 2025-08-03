#!/usr/bin/env python3
# backend/run_bert_tests.py
"""
BERT Implementation Test Runner
Run this script from the backend/ directory to test BERT implementation
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path for app imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the test
try:
    from app.scripts.test_bert_implementation import main
    
    if __name__ == "__main__":
        print("🚀 Running BERT Implementation Tests...")
        print(f"📁 Working directory: {current_dir}")
        print(f"🐍 Python path: {sys.path[0]}")
        print("-" * 50)
        
        success = main()
        
        if success:
            print("\n✅ All tests completed successfully!")
        else:
            print("\n❌ Some tests failed. Check output above.")
            
        sys.exit(0 if success else 1)
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure you're running this from the backend/ directory")
    print("2. Check that all BERT implementation files exist:")
    print("   - app/nlp/bert_priority_classifier.py")
    print("   - app/nlp/bert_training_data_generator.py") 
    print("   - app/nlp/bert_trainer.py")
    print("   - app/services/conflict_detector.py")
    print("3. Install dependencies: pip install -r requirements/base.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    sys.exit(1)
