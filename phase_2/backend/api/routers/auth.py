"""
Authentication endpoints for the Todo Web Application with rate limiting.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from datetime import timedelta
from sqlmodel import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from models.user import User, UserCreate, UserRead
from database import get_session
from core.security import verify_password, get_password_hash, create_access_token, get_current_user
from schemas.auth import Token, UserRegister, UserLogin
from services.user_service import get_user_by_email

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.post("/register", response_model=Token)
@limiter.limit("5/minute")  # Limit to 5 registrations per minute per IP
async def register(request: Request, user_data: UserRegister, session: Session = Depends(get_session)):
    """
    Register a new user.

    Args:
        user_data: User registration data
        session: Database session

    Returns:
        Token: Access token for the newly registered user

    Raises:
        HTTPException: If email is already registered
    """
    # Check if user already exists
    existing_user = get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        password=hashed_password  # Now stored in the User model
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.id, "email": db_user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")  # Limit to 10 login attempts per minute per IP
async def login(request: Request, user_data: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token.

    Args:
        user_data: User login credentials
        session: Database session

    Returns:
        Token: Access token for the authenticated user

    Raises:
        HTTPException: If credentials are invalid
    """
    # Get user by email
    db_user = get_user_by_email(session, user_data.email)
    if not db_user or not verify_password(user_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.id, "email": db_user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user's information.

    Args:
        current_user: The currently authenticated user (extracted from token)

    Returns:
        UserRead: The current user's information
    """
    return current_user