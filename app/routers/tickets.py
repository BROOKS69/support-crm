"""
Ticket router for Support CRM Backend.

This module provides CRUD endpoints for managing support tickets,
including creation, retrieval, updating, and deletion of tickets.
All endpoints require authentication.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, database
from app.routers.utils import get_current_active_user

# Create the ticket router
router = APIRouter()

# Alias for database dependency
get_db = database.get_db

@router.get("/", response_model=List[schemas.TicketOut])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Retrieve a paginated list of support tickets.

    Args:
        skip: Number of tickets to skip (for pagination)
        limit: Maximum number of tickets to return
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        List[TicketOut]: List of ticket data
    """
    tickets = db.query(models.Ticket).offset(skip).limit(limit).all()
    return tickets

@router.post("/", response_model=schemas.TicketOut)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Create a new support ticket.

    Validates that the customer exists and (if provided) the assigned agent exists.

    Args:
        ticket: Ticket creation data
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        TicketOut: Created ticket data

    Raises:
        HTTPException: If customer or assigned agent not found
    """
    # Validate customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == ticket.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Validate assigned agent exists (if provided)
    if ticket.assigned_agent_id:
        agent = db.query(models.User).filter(models.User.id == ticket.assigned_agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Assigned agent not found")

    # Create ticket
    db_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status=ticket.status,
        customer_id=ticket.customer_id,
        assigned_agent_id=ticket.assigned_agent_id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/{ticket_id}", response_model=schemas.TicketOut)
def read_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Retrieve a specific support ticket by ID.

    Args:
        ticket_id: Ticket ID to retrieve
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        TicketOut: Ticket data

    Raises:
        HTTPException: If ticket not found
    """
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/{ticket_id}", response_model=schemas.TicketOut)
def update_ticket(ticket_id: int, ticket_update: schemas.TicketCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Update an existing support ticket.

    Validates that the customer and assigned agent (if provided) exist.

    Args:
        ticket_id: Ticket ID to update
        ticket_update: Updated ticket data
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        TicketOut: Updated ticket data

    Raises:
        HTTPException: If ticket, customer, or assigned agent not found
    """
    # Find existing ticket
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Validate customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == ticket_update.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Validate assigned agent exists (if provided)
    if ticket_update.assigned_agent_id:
        agent = db.query(models.User).filter(models.User.id == ticket_update.assigned_agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Assigned agent not found")

    # Update ticket fields
    ticket.title = ticket_update.title
    ticket.description = ticket_update.description
    ticket.priority = ticket_update.priority
    ticket.status = ticket_update.status
    ticket.customer_id = ticket_update.customer_id
    ticket.assigned_agent_id = ticket_update.assigned_agent_id

    db.commit()
    db.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Delete a support ticket.

    Args:
        ticket_id: Ticket ID to delete
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        dict: Success message

    Raises:
        HTTPException: If ticket not found
    """
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()
    return {"detail": "Ticket deleted successfully"}
