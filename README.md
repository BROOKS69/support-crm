# SupportCRM Backend

A robust, scalable REST API backend for a Customer Relationship Management (CRM) system focused on support ticket management. Built with FastAPI, SQLAlchemy, and modern Python practices.

## 🚀 Features

### Authentication & Authorization
- JWT-based authentication system
- Role-based access control (Agent, Admin)
- Secure user registration and login
- Password hashing with bcrypt

### Customer Management
- Complete CRUD operations for customer profiles
- Customer search and filtering capabilities
- Customer data validation and integrity

### Support Ticket Management
- Create and manage support tickets linked to customers
- Ticket status tracking (Open, In-Progress, Resolved)
- Priority levels and assignment to agents
- Timestamp tracking for SLA monitoring

### Communication Logs
- Record all customer interactions (calls, emails, chats)
- Associate logs with specific tickets and customers
- Audit trail for compliance and quality assurance

### Analytics & Reporting
- Ticket metrics and performance reports
- Agent workload analysis
- Response time tracking
- Dashboard-ready JSON responses

## 🛠 Tech Stack

- **Framework**: FastAPI - High-performance async web framework
- **Database**: SQLAlchemy ORM with SQLite (easily configurable for PostgreSQL/MySQL)
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt via passlib
- **Validation**: Pydantic models
- **Documentation**: Automatic OpenAPI/Swagger UI generation
- **Development**: Uvicorn ASGI server

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BROOKS69/supportcrm-main
   cd supportcrm
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

The API will be available at `http://127.0.0.1:8000`

## 📖 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://127.0.0.1:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://127.0.0.1:8000/redoc` (ReDoc)
- **OpenAPI Schema**: `http://127.0.0.1:8000/openapi.json`

## 🔐 Authentication

### Register a new user
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "agent1", "email": "agent@example.com", "password": "securepass", "role": "agent"}'
```

### Login
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=agent1&password=securepass"
```

Use the returned `access_token` in the Authorization header for authenticated requests:
```
Authorization: Bearer <access_token>
```

## 🎯 Usage Examples

### Create a Customer
```bash
curl -X POST "http://127.0.0.1:8000/customers/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890", "company": "ABC Corp"}'
```

### Get All Customers
```bash
curl -X GET "http://127.0.0.1:8000/customers/" \
     -H "Authorization: Bearer <token>"
```

### Create a Support Ticket
```bash
curl -X POST "http://127.0.0.1:8000/tickets/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{"title": "Login Issue", "description": "User cannot login", "priority": "high", "customer_id": 1}'
```

## 🏗 Project Structure

```
supportcrm/
├── app/
│   ├── main.py              # FastAPI application instance
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── routers/
│       ├── customers.py     # Customer management
│       ├── tickets.py       # Ticket management
│       ├── logs.py          # Communication logs
│       └── reports.py       # Analytics & reporting
├── auth.py                  # Authentication endpoints
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── crm.db                 # SQLite database (auto-generated)
```

## 🧪 Testing

Run the development server and use the interactive API documentation at `/docs` to test endpoints manually, or use tools like Postman, Insomnia, or curl commands.

### Running Tests

```bash
# Run all tests
pytest test_api.py -v

# Run with coverage
pytest test_api.py --cov=app --cov-report=html
```

## 🔧 Troubleshooting

### Database Schema Issues

If you encounter errors like "no such column: tickets.assigned_agent_id", the database schema is out of sync with the models:

**Solution 1: Reset Database (Development Only)**
```bash
# Stop the server first
# Delete the database file
rm crm.db

# Restart the server - it will recreate tables automatically
uvicorn app.main:app --reload
```

**Solution 2: Run Migration Script (Recommended)**
```bash
# Run the migration script to add missing columns
python migrate_db.py

# Restart the server
uvicorn app.main:app --reload
```

**Solution 3: Manual Migration (Production)**
For production environments, use proper database migration tools like Alembic.

### Authentication Issues

- Ensure JWT tokens are included in Authorization headers as `Bearer <token>`
- Tokens expire after 30 minutes by default
- Check user roles for access control

### Common Errors

- **422 Unprocessable Entity**: Check request data format and required fields
- **401 Unauthorized**: Verify JWT token validity and format
- **404 Not Found**: Confirm endpoint URLs and HTTP methods
- **500 Internal Server Error**: Check server logs for detailed error information

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- CORS middleware (configurable)
- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy ORM

## 🚀 Deployment

### Production Considerations

1. **Database**: Switch from SQLite to PostgreSQL/MySQL
2. **Environment Variables**: Use `.env` files for sensitive configuration
3. **HTTPS**: Enable SSL/TLS in production
4. **Logging**: Implement structured logging
5. **Monitoring**: Add health checks and metrics

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team at email: devtoolsconglomerate.services@gmail.com or dosoowisdom1@gmail.com

---

**Built with ❤️ using FastAPI**
