#!/bin/bash

# KairoCal Repository Structure Setup Script
# Run this script inside your existing cloned GitHub repository

echo "🚀 Setting up KairoCal project structure in existing repository..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: This doesn't appear to be a git repository."
    echo "📋 Please run this script from inside your cloned KairoCal repository:"
    echo "   git clone <your-repo-url>"
    echo "   cd kairocal"
    echo "   bash setup-script.sh"
    exit 1
fi

echo "✅ Working in existing Git repository"

# Create GitHub-related directories
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE

# Create backend structure
mkdir -p backend/app/{api,core,models,schemas,services,nlp}
mkdir -p backend/app/nlp/models
mkdir -p backend/tests/{test_api,test_services,test_nlp}
mkdir -p backend/alembic/versions
mkdir -p backend/scripts
mkdir -p backend/requirements

# Create frontend structure
mkdir -p frontend/public
mkdir -p frontend/src/{components,pages,services,store,utils,config}
mkdir -p frontend/src/components/{auth,calendar,input,layout,common}
mkdir -p frontend/tests/{components,services}

# Create infrastructure structure
mkdir -p infrastructure/terraform/{modules,environments}
mkdir -p infrastructure/terraform/modules/{cognito,rds,eks,s3,cloudfront}
mkdir -p infrastructure/terraform/environments/{dev,prod}
mkdir -p infrastructure/k8s/{backend,frontend}
mkdir -p infrastructure/scripts

# Create documentation structure
mkdir -p docs/{architecture,api,deployment,user-guide}
mkdir -p docs/architecture/{decisions,diagrams}

# Create scripts directory
mkdir -p scripts

echo "📁 Directory structure created!"

# Create essential files
echo "📝 Creating essential files..."

# Root level files
touch README.md
touch LICENSE
touch CONTRIBUTING.md
touch Makefile
touch docker-compose.yml

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env
.venv
*.egg-info/
dist/
build/

# Node
node_modules/
dist/
build/
.env.local
.env.*.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDEs
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# AWS
.aws/
*.pem

# Terraform
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl

# Testing
coverage/
.coverage
htmlcov/
.pytest_cache/
.nyc_output/

# Logs
logs/
*.log

# OS
Thumbs.db
.DS_Store

# Project specific
backend/app/config/local_settings.py
frontend/src/config/local_config.js
EOF

# Create .dockerignore
cat > .dockerignore << 'EOF'
node_modules
npm-debug.log
Dockerfile*
.dockerignore
.git
.gitignore
README.md
.env
.nyc_output
coverage
.nyc_output
.coverage
htmlcov/
.pytest_cache/
__pycache__
EOF

# Backend files
echo "🐍 Creating backend files..."

# Backend requirements
cat > backend/requirements/base.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
pydantic==2.5.0
python-multipart==0.0.6
boto3==1.29.7
pydantic-settings==2.1.0
transformers==4.35.2
torch==2.1.1
spacy==3.7.2
celery==5.3.4
redis==5.0.1
EOF

cat > backend/requirements/dev.txt << 'EOF'
-r base.txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
isort==5.12.0
mypy==1.7.1
httpx==0.25.2
EOF

cat > backend/requirements/prod.txt << 'EOF'
-r base.txt
gunicorn==21.2.0
EOF

# Backend main files
touch backend/app/__init__.py
touch backend/app/main.py
touch backend/app/config.py

# Backend API files
touch backend/app/api/__init__.py
touch backend/app/api/auth.py
touch backend/app/api/events.py
touch backend/app/api/users.py
touch backend/app/api/health.py

# Backend core files
touch backend/app/core/__init__.py
touch backend/app/core/auth.py
touch backend/app/core/database.py
touch backend/app/core/exceptions.py
touch backend/app/core/utils.py

# Backend models
touch backend/app/models/__init__.py
touch backend/app/models/user.py
touch backend/app/models/event.py
touch backend/app/models/reminder.py

# Backend schemas
touch backend/app/schemas/__init__.py
touch backend/app/schemas/user.py
touch backend/app/schemas/event.py
touch backend/app/schemas/auth.py

# Backend services
touch backend/app/services/__init__.py
touch backend/app/services/nlp_service.py
touch backend/app/services/event_service.py
touch backend/app/services/notification_service.py
touch backend/app/services/conflict_detector.py

# Backend NLP
touch backend/app/nlp/__init__.py
touch backend/app/nlp/parser.py
touch backend/app/nlp/entity_extractor.py

# Backend tests
touch backend/tests/__init__.py
touch backend/tests/conftest.py

# Backend config files
touch backend/.env.example
touch backend/pytest.ini
touch backend/Dockerfile
touch backend/docker-compose.yml

# Alembic
touch backend/alembic/alembic.ini

echo "⚛️ Creating frontend files..."

# Frontend package.json placeholder
cat > frontend/package.json << 'EOF'
{
  "name": "kairocal-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "jest",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "vite": "^4.4.5"
  }
}
EOF

# Frontend files
touch frontend/public/index.html
touch frontend/public/favicon.ico
touch frontend/src/index.js
touch frontend/src/App.js
touch frontend/src/index.css

# Frontend components
touch frontend/src/components/auth/Login.jsx
touch frontend/src/components/auth/Register.jsx
touch frontend/src/components/auth/ProtectedRoute.jsx
touch frontend/src/components/calendar/Calendar.jsx
touch frontend/src/components/calendar/EventModal.jsx
touch frontend/src/components/calendar/EventList.jsx
touch frontend/src/components/input/NaturalLanguageInput.jsx
touch frontend/src/components/input/VoiceInput.jsx
touch frontend/src/components/layout/Header.jsx
touch frontend/src/components/layout/Sidebar.jsx
touch frontend/src/components/layout/Layout.jsx
touch frontend/src/components/common/Button.jsx
touch frontend/src/components/common/Modal.jsx
touch frontend/src/components/common/Notification.jsx

# Frontend pages
touch frontend/src/pages/Dashboard.jsx
touch frontend/src/pages/CalendarView.jsx
touch frontend/src/pages/Settings.jsx

# Frontend services
touch frontend/src/services/api.js
touch frontend/src/services/auth.js
touch frontend/src/services/events.js

# Frontend store
touch frontend/src/store/authStore.js
touch frontend/src/store/eventStore.js

# Frontend utils
touch frontend/src/utils/constants.js
touch frontend/src/utils/helpers.js
touch frontend/src/utils/validators.js

# Frontend config
touch frontend/src/config/aws-exports.js

# Frontend config files
touch frontend/.env.example
touch frontend/vite.config.js
touch frontend/tailwind.config.js
touch frontend/postcss.config.js
touch frontend/Dockerfile
touch frontend/.eslintrc.js

# Frontend tests
touch frontend/tests/setup.js

echo "☁️ Creating infrastructure files..."

# Terraform files
touch infrastructure/terraform/main.tf
touch infrastructure/terraform/variables.tf
touch infrastructure/terraform/outputs.tf

# Terraform modules
touch infrastructure/terraform/modules/cognito/main.tf
touch infrastructure/terraform/modules/cognito/variables.tf
touch infrastructure/terraform/modules/cognito/outputs.tf
touch infrastructure/terraform/modules/rds/main.tf
touch infrastructure/terraform/modules/rds/variables.tf
touch infrastructure/terraform/modules/rds/outputs.tf
touch infrastructure/terraform/modules/eks/main.tf
touch infrastructure/terraform/modules/eks/variables.tf
touch infrastructure/terraform/modules/eks/outputs.tf
touch infrastructure/terraform/modules/s3/main.tf
touch infrastructure/terraform/modules/s3/variables.tf
touch infrastructure/terraform/modules/s3/outputs.tf
touch infrastructure/terraform/modules/cloudfront/main.tf
touch infrastructure/terraform/modules/cloudfront/variables.tf
touch infrastructure/terraform/modules/cloudfront/outputs.tf

# Environment-specific terraform
touch infrastructure/terraform/environments/dev/main.tf
touch infrastructure/terraform/environments/dev/variables.tf
touch infrastructure/terraform/environments/prod/main.tf
touch infrastructure/terraform/environments/prod/variables.tf

# Kubernetes files
touch infrastructure/k8s/backend/deployment.yaml
touch infrastructure/k8s/backend/service.yaml
touch infrastructure/k8s/backend/configmap.yaml
touch infrastructure/k8s/frontend/deployment.yaml
touch infrastructure/k8s/frontend/service.yaml
touch infrastructure/k8s/ingress.yaml

# Infrastructure scripts
touch infrastructure/scripts/deploy.sh
touch infrastructure/scripts/rollback.sh
chmod +x infrastructure/scripts/*.sh

echo "📚 Creating documentation files..."

# Documentation
touch docs/architecture/README.md
touch docs/api/openapi.yaml
touch docs/deployment/README.md
touch docs/user-guide/README.md

echo "🔧 Creating GitHub workflow files..."

# GitHub workflows
cat > .github/workflows/backend-ci.yml << 'EOF'
name: Backend CI

on:
  push:
    branches: [ main, develop ]
    paths: [ 'backend/**' ]
  pull_request:
    branches: [ main ]
    paths: [ 'backend/**' ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements/dev.txt
        
    - name: Run tests
      run: |
        cd backend
        pytest --cov=app --cov-report=xml
        
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
EOF

cat > .github/workflows/frontend-ci.yml << 'EOF'
name: Frontend CI

on:
  push:
    branches: [ main, develop ]
    paths: [ 'frontend/**' ]
  pull_request:
    branches: [ main ]
    paths: [ 'frontend/**' ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
        
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
        
    - name: Run tests
      run: |
        cd frontend
        npm test
        
    - name: Build
      run: |
        cd frontend
        npm run build
EOF

touch .github/workflows/deploy.yml

# GitHub issue templates
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. iOS]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]

**Additional context**
Add any other context about the problem here.
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
EOF

echo "📝 Creating utility scripts..."

# Utility scripts
cat > scripts/setup-dev.sh << 'EOF'
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
EOF

cat > scripts/run-tests.sh << 'EOF'
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
EOF

cat > scripts/clean-repo.sh << 'EOF'
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
EOF

chmod +x scripts/*.sh

# Create Makefile
cat > Makefile << 'EOF'
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
EOF

# Create initial README
cat > README.md << 'EOF'
# KairoCal: AI-Powered Smart Calendar

An intelligent, cloud-native calendar application that processes natural language input to create and manage events automatically.

## 🚀 Features

- **Natural Language Processing**: Create events using voice or text input
- **Smart Scheduling**: Intelligent conflict detection and resolution
- **Cloud-Native**: Built on AWS with modern DevOps practices
- **Responsive UI**: Modern React interface with Tailwind CSS
- **Secure Authentication**: AWS Cognito integration

## 🏗️ Architecture

- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **NLP**: Hugging Face Transformers + spaCy
- **Cloud**: AWS (EKS, RDS, S3, CloudFront, Cognito)
- **DevOps**: Docker + Terraform + GitHub Actions

## 🛠️ Quick Start

1. **Setup Environment**
   ```bash
   make setup
   ```

2. **Run Development Servers**
   ```bash
   # Terminal 1 - Backend
   make dev-backend
   
   # Terminal 2 - Frontend  
   make dev-frontend
   ```

3. **Run Tests**
   ```bash
   make test
   ```

## 📁 Project Structure

```
kairocal/
├── backend/           # FastAPI application
├── frontend/          # React application
├── infrastructure/    # Terraform & K8s configs
├── docs/             # Documentation
└── scripts/          # Utility scripts
```

## 📚 Documentation

- [Technical Architecture](docs/architecture/README.md)
- [API Documentation](docs/api/openapi.yaml)
- [Deployment Guide](docs/deployment/README.md)
- [User Guide](docs/user-guide/README.md)

## 🧪 Testing

- Backend: pytest with 70%+ coverage
- Frontend: Jest + React Testing Library
- Integration: Postman collections
- E2E: Cypress (coming soon)

## 🚀 Deployment

The application is deployed on AWS using:
- **EKS**: Container orchestration
- **RDS**: PostgreSQL database
- **S3 + CloudFront**: Static file hosting
- **Cognito**: User authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Jyothi Mani Ravi Sankar**  
Master's Dissertation Project  
University of Liverpool  
Department of Computer Science
EOF

echo ""
echo "🎉 KairoCal project structure setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Run: make setup"
echo "2. Add your preserved Cognito config to frontend/src/config/aws-exports.js"
echo "3. Commit and push changes:"
echo "   git add ."
echo "   git commit -m 'feat: Complete project structure with FastAPI backend and React frontend'"
echo "   git push origin main"
echo ""
echo "🔧 Development workflow:"
echo "1. make dev-backend  (Terminal 1)"
echo "2. make dev-frontend (Terminal 2)"
echo "3. Open http://localhost:5173"
echo ""
echo "📁 Don't forget to:"
echo "• Copy your Cognito backup to frontend/src/config/aws-exports.js"
echo "• Update any environment variables in .env files"
echo ""
echo "Happy coding! 🚀"