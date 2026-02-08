"""
Authentication schemas for the Todo Web Application.
"""

from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for JWT token data.
    """
    email: str | None = None


class UserRegister(BaseModel):
    """
    Schema for user registration.
    """
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: str
    password: str