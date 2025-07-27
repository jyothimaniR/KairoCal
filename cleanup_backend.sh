#!/bin/bash

echo "🧹 Listing all empty files and folders in backend (excluding venv and __init__.py)..."

cd backend

echo ""
echo "🗑️ Empty files (excluding __init__.py):"
find . -path ./venv -prune -o -type f -empty -not -name "__init__.py" -print

echo ""
echo "📁 Empty directories:"
find . -path ./venv -prune -o -type d -empty -print

echo ""
echo "✅ Listing complete!"
