# Support CRM Backend

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive backend system built with Python and FastAPI that provides secure RESTful APIs for managing customer support interactions. This CRM backend enables efficient customer relationship management with features for authentication, ticket tracking, communication logging, and analytics.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Database](#database)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication system
- Role-based access control (Agent, Admin)
- Secure password hashing with bcrypt
- Token-based API access

### 👥 Customer Management
- Complete CRUD operations for customer profiles
- Customer search and filtering capabilities
- Customer data validation and integrity

### 🎫 Support Ticket System
- Create and manage support tickets
- Priority levels (Low, Medium, High, Urgent)
- Status tracking (Open, In-Progress, Resolved, Closed)
- Agent assignment functionality

### 📝 Communication Logs
- Track all customer interactions
- Support for multiple communication types (Call, Email, Chat)
- Timestamped log entries
- Ticket association for context

### 📊 Analytics & Reporting
- Ticket status summaries
- Agent workload distribution
- Response time analytics
- Dashboard-ready JSON responses

## 🛠 Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- **Authentication**: [PyJWT](https://pyjwt.readthedocs.io/) - JSON Web Token implementation
- **Password Hashing**: [Passlib](https://passlib.readthedocs.io/) - Secure password hashing
- **Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and serialization
- **Documentation**: [Swagger UI](https://swagger.io/tools/swagger-ui/) - Interactive API documentation

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- SQLite (included with Python) or PostgreSQL/MySQL for production

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/BROOKS69/support-crm-backend.git
cd support-crm-backend
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r app/requirements.txt
```

### 4. Initialize Database

```bash
python migrate_db.py
```

This will create the necessary database tables and set up the initial schema.

## 🎯 Usage

### Development Server

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### Production Deployment

For production deployment, use a production ASGI server:

```bash
# Using Gunicorn with Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📚 API Documentation

Once the server is running, access the comprehensive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | POST | User authentication |
| `/auth/register` | POST | User registration |
| `/customers` | GET/POST | Customer management |
| `/tickets` | GET/POST | Ticket operations |
| `/logs` | GET/POST | Communication logs |
| `/reports/tickets-summary` | GET | Analytics data |

## 🏗 Project Structure

```
support-crm-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application instance
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── customers.py     # Customer management
│       ├── tickets.py       # Ticket operations
│       ├── logs.py          # Communication logs
│       ├── reports.py       # Analytics & reporting
│       └── utils.py         # Authentication utilities
├── crm.db                   # SQLite database (development)
├── migrate_db.py            # Database migration script
├── test_api.py              # API testing script
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🗄 Database

### Development
- **Database**: SQLite (`crm.db`)
- **Location**: Project root directory
- **Migration**: Run `python migrate_db.py`

### Production
For production environments, configure environment variables:

```bash
export DATABASE_URL="postgresql://user:password@localhost/crm_db"
# or
export DATABASE_URL="mysql://user:password@localhost/crm_db"
```

## 🧪 Testing

Run the included test suite:

```bash
python test_api.py
```

This will test all major API endpoints and ensure functionality.

## 🚢 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

Create a `.env` file for configuration:

```env
DATABASE_URL=sqlite:///./crm.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Project Maintainer**: [BROOKS]

- **Email**: dosoowisdom1@gmail.com
- **GitHub**: [@BROOKS69](https://github.com/BROOKS69)
- **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/wisdomdosoo1)

---

⭐ **Star this repository** if you find it helpful!

*Built with ❤️ using FastAPI and Python*
