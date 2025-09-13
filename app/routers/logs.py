"""
Communication logs router for Support CRM Backend.

This module provides CRUD endpoints for managing communication logs,
which track customer interactions (calls, emails, chats) associated with support tickets.
All endpoints require authentication.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, database
from app.routers.utils import get_current_active_user

# Create the logs router
router = APIRouter()

# Alias for database dependency
get_db = database.get_db

@router.get("/", response_model=List[schemas.LogOut])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Retrieve a paginated list of communication logs.

    Args:
        skip: Number of logs to skip (for pagination)
        limit: Maximum number of logs to return
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        List[LogOut]: List of communication log data
    """
    logs = db.query(models.Log).offset(skip).limit(limit).all()
    return logs

@router.post("/", response_model=schemas.LogOut)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Create a new communication log entry.

    Validates that the associated ticket exists before creating the log.

    Args:
        log: Log creation data
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        LogOut: Created log data

    Raises:
        HTTPException: If associated ticket not found
    """
    # Validate ticket exists
    ticket = db.query(models.Ticket).filter(models.Ticket.id == log.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Create log entry
    db_log = models.Log(
        type=log.type,
        content=log.content,
        ticket_id=log.ticket_id
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/{log_id}", response_model=schemas.LogOut)
def read_log(log_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Retrieve a specific communication log by ID.

    Args:
        log_id: Log ID to retrieve
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        LogOut: Log data

    Raises:
        HTTPException: If log not found
    """
    log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@router.put("/{log_id}", response_model=schemas.LogOut)
def update_log(log_id: int, log_update: schemas.LogCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Update an existing communication log.

    Validates that the associated ticket exists.

    Args:
        log_id: Log ID to update
        log_update: Updated log data
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        LogOut: Updated log data

    Raises:
        HTTPException: If log or associated ticket not found
    """
    # Find existing log
    log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    # Validate ticket exists
    ticket = db.query(models.Ticket).filter(models.Ticket.id == log_update.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update log fields
    log.type = log_update.type
    log.content = log_update.content
    log.ticket_id = log_update.ticket_id

    db.commit()
    db.refresh(log)
    return log

@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Delete a communication log entry.

    Args:
        log_id: Log ID to delete
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        dict: Success message

    Raises:
        HTTPException: If log not found
    """
    log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(log)
    db.commit()
    return {"detail": "Log deleted successfully"}
