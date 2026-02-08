"""
JWT verification middleware for the Todo Web Application.
"""

from fastapi import HTTPException, status, Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import json

from ..utils.token import verify_token


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer authentication scheme that verifies tokens.
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[dict]:
        """
        Verify the JWT token from the Authorization header.

        Args:
            request: The incoming request

        Returns:
            Optional[dict]: The decoded token payload if valid, raises HTTPException if invalid

        Raises:
            HTTPException: If the token is invalid or missing
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Wrong authentication scheme. Use Bearer."
                )

            token = credentials.credentials

            # Verify the token
            payload = verify_token(token)
            if payload is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired token"
                )

            return payload
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authentication credentials were not provided"
            )


def get_current_user_from_token(token_payload: dict) -> str:
    """
    Extract the current user ID from the token payload.

    Args:
        token_payload: The decoded token payload

    Returns:
        str: The user ID from the token

    Raises:
        HTTPException: If the user ID is not found in the token
    """
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials - no user ID in token"
        )

    return user_id


def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """
    Verify that a user owns a specific resource.

    Args:
        user_id: The ID of the user making the request
        resource_user_id: The ID of the user who owns the resource

    Returns:
        bool: True if the user owns the resource, False otherwise
    """
    return user_id == resource_user_id