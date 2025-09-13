"""
Main application module for Support CRM Backend.

This module initializes the FastAPI application, sets up database tables,
and includes all API routers for authentication, customers, tickets,
communication logs, and reports.
"""

from fastapi import FastAPI
from app import models, database, auth
from app.routers import customers, tickets, logs, reports

# Create all database tables defined in models (only if they don't exist)
# This ensures the database schema is up to date on application startup
# Note: In production, use proper database migrations (Alembic)
from sqlalchemy import inspect

# Check if tables already exist to avoid unnecessary recreation during reloads
inspector = inspect(database.engine)
existing_tables = inspector.get_table_names()

if not existing_tables:  # Only create tables if database is empty
    models.Base.metadata.create_all(bind=database.engine)
    print("Database tables created successfully")
else:
    print("Database tables already exist, skipping creation")

# Initialize FastAPI application with title for API documentation
app = FastAPI(title="Support CRM Backend")

# Include authentication router for user login, registration, and profile
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include customers router for CRUD operations on customer profiles
app.include_router(customers.router, prefix="/customers", tags=["Customers"])

# Include tickets router for support ticket management
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])

# Include logs router for communication log management
app.include_router(logs.router, prefix="/logs", tags=["Communication Logs"])

# Include reports router for analytics and reporting endpoints
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to Support CRM Backend API"}
