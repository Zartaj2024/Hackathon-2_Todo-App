"""
Token utilities for the Todo Web Application.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from ..config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time for the token

    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the decoded payload.

    Args:
        token: The JWT token to verify

    Returns:
        Optional[dict]: The decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def decode_token_payload(token: str) -> Optional[dict]:
    """
    Decode a JWT token without verifying its signature.
    WARNING: Only use this for non-security-sensitive operations.

    Args:
        token: The JWT token to decode

    Returns:
        Optional[dict]: The decoded token payload, None if decoding fails
    """
    try:
        # This decodes without verification - use carefully!
        payload = jwt.decode(
            token, options={"verify_signature": False}
        )
        return payload
    except JWTError:
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired.

    Args:
        token: The JWT token to check

    Returns:
        bool: True if the token is expired, False otherwise
    """
    payload = verify_token(token)
    if not payload:
        return True  # Invalid token is treated as expired

    exp_time = payload.get("exp")
    if not exp_time:
        return True  # Token without expiration is treated as expired

    return datetime.utcnow().timestamp() > exp_time