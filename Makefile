.PHONY: help dev-backend dev-frontend dev test clean setup

help:
	@echo "Available commands:"
	@echo "  make setup        - Set up development environment"
	@echo "  make dev-backend  - Run backend development server"
	@echo "  make dev-frontend - Run frontend development server"
	@echo "  make dev          - Run both servers (requires 2 terminals)"
	@echo "  make test         - Run all tests"
	@echo "  make clean        - Clean up generated files"

setup:
	@bash scripts/setup-dev.sh

dev-backend:
	cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

dev:
	@echo "Starting both servers..."
	@echo "Open 2 terminals and run:"
	@echo "Terminal 1: make dev-backend"
	@echo "Terminal 2: make dev-frontend"

test:
	@bash scripts/run-tests.sh

clean:
	@bash scripts/clean-repo.sh
