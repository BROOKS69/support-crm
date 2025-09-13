"""
Main application module for Support CRM Backend.

This module initializes the FastAPI application, sets up database tables,
and includes all API routers for authentication, customers, tickets,
communication logs, and reports.
"""

from fastapi import FastAPI
from app import models, database, auth
from app.routers import customers, tickets, logs, reports

# Create all database tables defined in models
# This ensures the database schema is up to date on application startup
models.Base.metadata.create_all(bind=database.engine)

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
