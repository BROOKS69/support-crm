"""
Database models for Support CRM Backend.

This module defines SQLAlchemy ORM models for Users, Customers, Tickets, and Logs.
These models represent the core entities in the customer support CRM system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    """
    User model representing support agents and administrators.

    Attributes:
        id: Primary key
        username: Unique username for login
        email: Unique email address
        hashed_password: Bcrypt hashed password
        role: User role ('agent' or 'admin')
        is_active: Account status flag
        assigned_tickets: Relationship to tickets assigned to this user
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="agent")  # agent, admin
    is_active = Column(String, default=True)

    # Relationship: One user can have many assigned tickets
    assigned_tickets = relationship("Ticket", back_populates="assigned_agent")

class Customer(Base):
    """
    Customer model representing client information.

    Attributes:
        id: Primary key
        name: Customer full name
        email: Unique email address
        phone: Contact phone number
        company: Company name
        notes: Additional notes about the customer
        tickets: Relationship to customer's support tickets
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationship: One customer can have many tickets
    tickets = relationship("Ticket", back_populates="customer")

class Ticket(Base):
    """
    Support ticket model representing customer support requests.

    Attributes:
        id: Primary key
        title: Ticket title/summary
        description: Detailed description of the issue
        priority: Priority level ('low', 'medium', 'high', 'urgent')
        status: Current status ('open', 'in-progress', 'resolved', 'closed')
        created_at: Timestamp when ticket was created
        customer_id: Foreign key to customer
        assigned_agent_id: Foreign key to assigned agent (nullable)
        customer: Relationship to customer
        logs: Relationship to communication logs
        assigned_agent: Relationship to assigned agent
    """
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="medium")
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="tickets")
    logs = relationship("Log", back_populates="ticket")
    assigned_agent = relationship("User", back_populates="assigned_tickets")

class Log(Base):
    """
    Communication log model for tracking customer interactions.

    Attributes:
        id: Primary key
        type: Type of communication ('call', 'email', 'chat')
        content: Content/details of the communication
        created_at: Timestamp when log was created
        ticket_id: Foreign key to associated ticket
        ticket: Relationship to ticket
    """
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # call, email, chat
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))

    # Relationship: One ticket can have many logs
    ticket = relationship("Ticket", back_populates="logs")
