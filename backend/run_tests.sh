#!/bin/bash
# backend/run_tests.sh  
# Unix/Linux shell script to run BERT tests with proper Python path

echo "Setting up Python path for KairoCal backend..."
export PYTHONPATH=$(pwd)
echo "PYTHONPATH set to: $PYTHONPATH"

echo ""
echo "Running BERT implementation tests..."
python app/scripts/test_bert_implementation.py
