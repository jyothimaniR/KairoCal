#!/usr/bin/env python3
"""
Model Download Script for KairoCal
Downloads required ML models for local development
"""

import os
import sys
import requests
from pathlib import Path
from huggingface_hub import hf_hub_download
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_model_directory():
    """Create model directory if it doesn't exist"""
    model_dir = Path("backend/models/bert_priority_classifier")
    model_dir.mkdir(parents=True, exist_ok=True)
    return model_dir

def download_bert_model():
    """Download BERT model from Hugging Face Hub"""
    model_dir = create_model_directory()
    
    try:
        logger.info("Downloading BERT model for priority classification...")
        
        # Download model files
        files_to_download = [
            "pytorch_model.bin",
            "config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "vocab.txt"
        ]
        
        model_name = "bert-base-uncased"
        
        for file_name in files_to_download:
            try:
                file_path = hf_hub_download(
                    repo_id=model_name,
                    filename=file_name,
                    cache_dir=str(model_dir)
                )
                logger.info(f"Downloaded {file_name}")
            except Exception as e:
                logger.warning(f"Could not download {file_name}: {e}")
        
        logger.info("✅ BERT model download completed!")
        
    except Exception as e:
        logger.error(f"❌ Error downloading BERT model: {e}")
        logger.info("The application will use fallback classification methods.")

def create_model_readme():
    """Create README for model management"""
    readme_content = """# KairoCal ML Models

This directory contains machine learning models used by KairoCal.

## Model Files (Not in Git)

Due to GitHub's 100MB file size limit, ML model files are not stored in the repository.

### Required Models:

1. **BERT Priority Classifier** (`bert_priority_classifier/`)
   - `pytorch_model.bin` (254MB) - Main BERT model weights
   - `config.json` - Model configuration
   - `tokenizer.json` - Tokenizer configuration
   - `vocab.txt` - Vocabulary file

## Setup Instructions

### Option 1: Download Script (Recommended)
```bash
# From project root
python scripts/download_models.py
```

### Option 2: Manual Download
Download from [Hugging Face BERT base uncased](https://huggingface.co/bert-base-uncased)

### Option 3: Alternative Model Storage
For production deployments, consider:
- **AWS S3** with model versioning
- **Google Cloud Storage** 
- **Azure Blob Storage**
- **Git LFS** for team sharing

## Fallback Behavior

If models are not available, KairoCal will:
1. Use keyword-based priority classification
2. Log warnings about missing models
3. Continue functioning with reduced ML capabilities

## Model Management Best Practices

1. **Version Control**: Track model versions separately
2. **Environment Variables**: Configure model paths
3. **Health Checks**: Verify model availability on startup
4. **Graceful Degradation**: Fallback to simpler methods

## File Sizes
- `pytorch_model.bin`: ~254MB
- Total model directory: ~260MB
"""
    
    readme_path = Path("backend/models/README.md")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    logger.info("✅ Created model README.md")

if __name__ == "__main__":
    logger.info("🚀 Starting KairoCal model download...")
    create_model_readme()
    download_bert_model()
    logger.info("🎉 Model setup completed!")
