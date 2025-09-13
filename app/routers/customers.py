"""
Customer router for Support CRM Backend.

This module provides CRUD endpoints for managing customer profiles,
including creation and retrieval of customer data.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

# Create the customer router
router = APIRouter()

@router.post("/", response_model=schemas.CustomerOut)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    """
    Create a new customer profile.

    Args:
        customer: Customer creation data
        db: Database session dependency

    Returns:
        CustomerOut: Created customer data
    """
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/", response_model=list[schemas.CustomerOut])
def get_customers(db: Session = Depends(database.get_db)):
    """
    Retrieve a list of all customers.

    Args:
        db: Database session dependency

    Returns:
        List[CustomerOut]: List of customer profiles
    """
    return db.query(models.Customer).all()
