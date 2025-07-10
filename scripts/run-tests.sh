#!/bin/bash

echo "🧪 Running all tests..."

# Backend tests
echo "🐍 Running backend tests..."
cd backend
source venv/bin/activate 2>/dev/null || venv\Scripts\activate 2>/dev/null
pytest --cov=app --cov-report=term-missing
cd ..

# Frontend tests
echo "⚛️ Running frontend tests..."
cd frontend
npm test -- --coverage
cd ..

echo "✅ All tests completed!"
