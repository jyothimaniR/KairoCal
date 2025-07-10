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
