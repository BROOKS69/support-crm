"""
Customer router for Support CRM Backend.

This module provides CRUD endpoints for managing customer profiles,
including creation, retrieval, update, and deletion of customer data.
All endpoints require authentication.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.routers.utils import get_current_active_user

# Create the customer router
router = APIRouter()

@router.post("/", response_model=schemas.CustomerOut)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new customer profile.

    Requires authentication. Only authenticated users can create customers.

    Args:
        customer: Customer creation data
        db: Database session dependency
        current_user: Current authenticated user dependency

    Returns:
        CustomerOut: Created customer data
    """
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/", response_model=list[schemas.CustomerOut])
def get_customers(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Retrieve a list of all customers.

    Requires authentication. Only authenticated users can view customers.

    Args:
        db: Database session dependency
        current_user: Current authenticated user dependency

    Returns:
        List[CustomerOut]: List of customer profiles
    """
    return db.query(models.Customer).all()

@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(
    customer_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Retrieve a specific customer by ID.

    Requires authentication. Only authenticated users can view customer details.

    Args:
        customer_id: ID of the customer to retrieve
        db: Database session dependency
        current_user: Current authenticated user dependency

    Returns:
        CustomerOut: Customer profile data

    Raises:
        HTTPException: If customer not found
    """
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(
    customer_id: int,
    customer_update: schemas.CustomerUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update an existing customer profile.

    Requires authentication. Only authenticated users can update customers.

    Args:
        customer_id: ID of the customer to update
        customer_update: Updated customer data
        db: Database session dependency
        current_user: Current authenticated user dependency

    Returns:
        CustomerOut: Updated customer data

    Raises:
        HTTPException: If customer not found
    """
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Update customer fields
    for field, value in customer_update.dict(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete a customer profile.

    Requires authentication. Only authenticated users can delete customers.

    Args:
        customer_id: ID of the customer to delete
        db: Database session dependency
        current_user: Current authenticated user dependency

    Returns:
        dict: Success message

    Raises:
        HTTPException: If customer not found
    """
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}
