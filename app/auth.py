"""
Authentication router for Support CRM Backend.

This module provides JWT-based authentication endpoints including user registration,
login, and profile retrieval. It handles password hashing, token generation,
and user validation.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database, models, schemas
from app.routers.utils import authenticate_user, create_access_token, get_current_active_user, get_password_hash

# Create the authentication router
router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Register a new user account.

    Checks for existing username and email, hashes the password,
    creates the user in the database, and returns the user data.

    Args:
        user: User creation data (username, email, password, role)
        db: Database session dependency

    Returns:
        UserOut: Created user data

    Raises:
        HTTPException: If username or email already exists
    """
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and create user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    # Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Authenticate user and return JWT access token.

    Validates username/password combination and generates a JWT token
    with 30-minute expiration.

    Args:
        form_data: OAuth2 form data with username and password
        db: Database session dependency

    Returns:
        Token: JWT access token and type

    Raises:
        HTTPException: If authentication fails
    """
    # Authenticate user credentials
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    """
    Get current authenticated user's profile information.

    Requires valid JWT token in Authorization header.

    Args:
        current_user: Current authenticated user (injected by dependency)

    Returns:
        UserOut: Current user's profile data
    """
    return current_user
