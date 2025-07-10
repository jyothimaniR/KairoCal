#!/bin/bash

echo "🧹 Cleaning repository..."

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Remove Node modules and build artifacts
rm -rf frontend/node_modules
rm -rf frontend/dist
rm -rf frontend/.next

# Remove coverage files
rm -rf backend/.coverage
rm -rf backend/htmlcov
rm -rf frontend/coverage

# Remove logs
find . -name "*.log" -delete

echo "✅ Repository cleaned!"
