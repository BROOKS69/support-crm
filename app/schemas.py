from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Auth Schemas
class UserBase(BaseModel):
    username: str
    email: str
    role: str = "agent"

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    notes: Optional[str]

class CustomerCreate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    id: int
    class Config:
        from_attributes = True

# Ticket Schemas
class TicketBase(BaseModel):
    title: str
    description: Optional[str]
    priority: str = "medium"
    status: str = "open"

class TicketCreate(TicketBase):
    customer_id: int

class TicketOut(TicketBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Log Schemas
class LogBase(BaseModel):
    type: str
    content: str

class LogCreate(LogBase):
    ticket_id: int

class LogOut(LogBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
