"""
Pydantic schemas for Support CRM Backend.

This module defines Pydantic BaseModel classes for request/response validation,
data serialization, and API documentation. These schemas ensure type safety
and automatic validation for all API endpoints.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ===== AUTH SCHEMAS =====

class UserBase(BaseModel):
    """
    Base schema for user data.

    Attributes:
        username: Unique username for authentication
        email: Unique email address
        role: User role ('agent' or 'admin'), defaults to 'agent'
    """
    username: str
    email: str
    role: str = "agent"

class UserCreate(UserBase):
    """
    Schema for user registration/creation requests.

    Extends UserBase with password field required for account creation.
    """
    password: str

class UserOut(UserBase):
    """
    Schema for user data in API responses.

    Includes additional fields returned to clients.
    """
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # Enable ORM model conversion

class Token(BaseModel):
    """
    Schema for JWT token response.

    Attributes:
        access_token: JWT access token string
        token_type: Token type (usually 'bearer')
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for decoded JWT token data.

    Attributes:
        username: Username extracted from token (optional)
    """
    username: Optional[str] = None

# ===== CUSTOMER SCHEMAS =====

class CustomerBase(BaseModel):
    """
    Base schema for customer data.

    Attributes:
        name: Customer full name
        email: Customer email address
        phone: Customer phone number (optional)
        company: Customer company name (optional)
        notes: Additional notes about the customer (optional)
    """
    name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    notes: Optional[str]

class CustomerCreate(CustomerBase):
    """
    Schema for customer creation requests.

    Inherits all fields from CustomerBase.
    """
    pass

class CustomerUpdate(BaseModel):
    """
    Schema for customer update requests.

    All fields are optional to allow partial updates.
    """
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None

class CustomerOut(CustomerBase):
    """
    Schema for customer data in API responses.

    Includes the customer ID.
    """
    id: int

    class Config:
        from_attributes = True  # Enable ORM model conversion

# ===== TICKET SCHEMAS =====

class TicketBase(BaseModel):
    """
    Base schema for ticket data.

    Attributes:
        title: Ticket title/summary
        description: Detailed description of the issue (optional)
        priority: Priority level ('low', 'medium', 'high', 'urgent')
        status: Current status ('open', 'in-progress', 'resolved', 'closed')
    """
    title: str
    description: Optional[str]
    priority: str = "medium"
    status: str = "open"

class TicketCreate(TicketBase):
    """
    Schema for ticket creation requests.

    Extends TicketBase with required customer and optional agent assignment.
    """
    customer_id: int
    assigned_agent_id: Optional[int] = None

class TicketOut(TicketBase):
    """
    Schema for ticket data in API responses.

    Includes additional fields returned to clients.
    """
    id: int
    created_at: datetime
    assigned_agent_id: Optional[int]

    class Config:
        from_attributes = True  # Enable ORM model conversion

# ===== LOG SCHEMAS =====

class LogBase(BaseModel):
    """
    Base schema for communication log data.

    Attributes:
        type: Type of communication ('call', 'email', 'chat')
        content: Content/details of the communication
    """
    type: str
    content: str

class LogCreate(LogBase):
    """
    Schema for log creation requests.

    Extends LogBase with required ticket association.
    """
    ticket_id: int

class LogOut(LogBase):
    """
    Schema for log data in API responses.

    Includes additional fields returned to clients.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM model conversion
