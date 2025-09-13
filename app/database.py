"""
Database configuration module for Support CRM Backend.

This module sets up the SQLAlchemy database engine, session management,
and provides a dependency for database sessions in FastAPI endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for SQLite (suitable for development/testing)
# In production, replace with PostgreSQL or other production database
DATABASE_URL = "sqlite:///./crm.db"

# Create SQLAlchemy engine with SQLite-specific connection arguments
# check_same_thread=False allows multiple threads to use the same connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configure session maker for database sessions
# autocommit=False: transactions must be committed explicitly
# autoflush=False: changes are not automatically flushed to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models to inherit from
Base = declarative_base()

def get_db():
    """
    Dependency function to provide database session to FastAPI endpoints.

    Yields a database session and ensures it is properly closed after use.
    This function is used as a dependency in route handlers.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
