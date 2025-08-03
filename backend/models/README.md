# KairoCal ML Models

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
