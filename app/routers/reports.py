"""
Reports and analytics router for Support CRM Backend.

This module provides endpoints for generating reports and analytics
on support ticket data, including ticket summaries, agent workload,
and response time metrics. All endpoints require authentication.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List

from app import models, database
from app.routers.utils import get_current_active_user

# Create the reports router
router = APIRouter()

# Alias for database dependency
get_db = database.get_db

@router.get("/tickets-summary")
def get_tickets_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Generate a summary report of ticket status counts.

    Counts tickets by status (open, in-progress, resolved) and provides totals.

    Args:
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        dict: Ticket summary with counts by status
    """
    # Count tickets by status
    open_count = db.query(models.Ticket).filter(models.Ticket.status == "open").count()
    in_progress_count = db.query(models.Ticket).filter(models.Ticket.status == "in-progress").count()
    resolved_count = db.query(models.Ticket).filter(models.Ticket.status == "resolved").count()

    # Calculate total
    total = open_count + in_progress_count + resolved_count

    return {
        "total_tickets": total,
        "open": open_count,
        "in_progress": in_progress_count,
        "resolved": resolved_count
    }

@router.get("/agent-workload")
def get_agent_workload(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Generate a report of ticket workload distribution among agents.

    Shows how many tickets are assigned to each agent.

    Args:
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        dict: Agent workload mapping (agent username -> ticket count)
    """
    # Query agent names and their assigned ticket counts
    # Using left outer join to include agents with zero tickets
    agent_counts = db.query(
        models.User.username,
        func.count(models.Ticket.id)
    ).join(
        models.Ticket,
        models.User.id == models.Ticket.assigned_agent_id,
        isouter=True
    ).group_by(models.User.id).all()

    return {"agent_workload": dict(agent_counts)}

@router.get("/response-times")
def get_response_times(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Generate response time analytics.

    Currently returns a placeholder value. In a full implementation,
    this would calculate average time from ticket creation to first response
    or resolution based on available timestamp data.

    Args:
        db: Database session dependency
        current_user: Current authenticated user

    Returns:
        dict: Response time metrics (placeholder implementation)
    """
    # TODO: Implement actual response time calculation
    # This would require additional timestamp fields in the database
    # such as first_response_at, resolved_at, etc.

    # For now, return a placeholder value
    return {"average_response_time_hours": 24.5}
