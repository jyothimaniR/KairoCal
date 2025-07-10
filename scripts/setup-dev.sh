#!/bin/bash

echo "🚀 Setting up KairoCal development environment..."

# Backend setup
echo "🐍 Setting up backend..."
cd backend
python -m venv venv
source venv/bin/activate || venv\Scripts\activate  # Windows compatibility
pip install -r requirements/dev.txt
cd ..

# Frontend setup
echo "⚛️ Setting up frontend..."
cd frontend
npm install
cd ..

echo "✅ Development environment setup complete!"
echo "📋 Next steps:"
echo "1. Activate Python venv: cd backend && source venv/bin/activate"
echo "2. Run backend: make dev-backend"
echo "3. Run frontend: make dev-frontend"
