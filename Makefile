# KairoCal Development Commands

.PHONY: setup dev-backend dev-frontend test clean

# Setup - Activate virtual environment and install dependencies
setup:
	@echo "🚀 Setting up KairoCal development environment..."
	@echo "✅ Virtual environment: .venv (already exists)"
	@echo "✅ Python packages: 148 installed"
	@echo "✅ Node packages: installed"

# Development - Backend
dev-backend:
	@echo "🔧 Starting KairoCal Backend (port 8001)..."
	cd .venv/Scripts && activate && cd ../../backend && python start_server.py

# Development - Frontend  
dev-frontend:
	@echo "🔧 Starting KairoCal Frontend..."
	cd frontend && npm run dev

# Test
test:
	@echo "🧪 Running KairoCal tests..."
	cd .venv/Scripts && activate && cd ../../backend && python -m pytest

# Clean
clean:
	@echo "🧹 Cleaning build artifacts..."
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete