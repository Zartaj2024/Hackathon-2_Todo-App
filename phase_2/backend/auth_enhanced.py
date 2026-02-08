"""
Enhanced authentication configuration for the Todo Web Application with comprehensive error handling.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from config import settings
from models.user import User
from database_enhanced import get_enhanced_session
from sqlmodel import Session
import secrets
import re
from enum import Enum


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthError(Enum):
    """Enumeration of authentication errors for consistent error handling."""
    INVALID_CREDENTIALS = "invalid_credentials"
    USER_NOT_FOUND = "user_not_found"
    USER_INACTIVE = "user_inactive"
    TOKEN_EXPIRED = "token_expired"
    TOKEN_INVALID = "token_invalid"
    PASSWORD_WEAK = "password_weak"
    EMAIL_INVALID = "email_invalid"
    USER_EXISTS = "user_exists"
    DATABASE_ERROR = "database_error"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"


class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, error_type: AuthError, message: str = None):
        self.error_type = error_type
        self.message = message or error_type.value
        super().__init__(self.message)


class AuthConfig:
    """Enhanced authentication configuration with comprehensive error handling."""

    def __init__(self):
        self._oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self._validate_config()

    @property
    def oauth2_scheme(self):
        return self._oauth2_scheme

    def _validate_config(self):
        """Validate authentication configuration."""
        errors = []

        if not settings.BETTER_AUTH_SECRET:
            errors.append("BETTER_AUTH_SECRET is not set")

        if not settings.JWT_SECRET_KEY:
            errors.append("JWT_SECRET_KEY is not set")

        if not settings.DATABASE_URL:
            errors.append("DATABASE_URL is not set")

        if errors:
            logger.error(f"Authentication configuration errors: {errors}")
            raise ValidationError(AuthError.DATABASE_ERROR, f"Configuration errors: {errors}")

    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = re.match(pattern, email) is not None
        if not is_valid:
            logger.warning(f"Invalid email format: {email}")
        return is_valid

    def validate_password(self, password: str) -> tuple[bool, str]:
        """Validate password strength and return (is_valid, reason)."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit"

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"

        return True, "Password is valid"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plaintext password against a hashed password with error handling."""
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            raise ValidationError(AuthError.INVALID_CREDENTIALS, "Password verification failed")

    def get_password_hash(self, password: str) -> str:
        """Hash a plaintext password with error handling."""
        try:
            # Validate password strength first
            is_valid, reason = self.validate_password(password)
            if not is_valid:
                raise ValidationError(AuthError.PASSWORD_WEAK, reason)

            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Password hashing error: {str(e)}")
            raise ValidationError(AuthError.DATABASE_ERROR, "Password hashing failed")

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token with enhanced error handling."""
        try:
            to_encode = data.copy()

            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

            to_encode.update({"exp": expire, "iat": datetime.utcnow(), "jti": secrets.token_urlsafe(16)})
            encoded_jwt = jwt.encode(
                to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
            )
            return encoded_jwt
        except Exception as e:
            logger.error(f"Token creation error: {str(e)}")
            raise ValidationError(AuthError.DATABASE_ERROR, "Token creation failed")

    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT refresh token with enhanced error handling."""
        try:
            to_encode = data.copy()

            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(days=7)  # Default to 7 days for refresh tokens

            to_encode.update({
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "refresh",
                "jti": secrets.token_urlsafe(16)
            })

            encoded_jwt = jwt.encode(
                to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
            )
            return encoded_jwt
        except Exception as e:
            logger.error(f"Refresh token creation error: {str(e)}")
            raise ValidationError(AuthError.DATABASE_ERROR, "Refresh token creation failed")

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify a JWT token and return the decoded payload with enhanced error handling."""
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            logger.warning(f"Token verification error: {str(e)}")
            raise ValidationError(AuthError.TOKEN_INVALID, "Token is invalid")
        except Exception as e:
            logger.error(f"Unexpected token verification error: {str(e)}")
            raise ValidationError(AuthError.DATABASE_ERROR, "Token verification failed")

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        """Dependency to get the current user from the token with enhanced error handling."""
        try:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            try:
                payload = jwt.decode(
                    token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
                )
                user_id: str = payload.get("sub")
                jti: str = payload.get("jti")  # Token identifier for potential revocation

                if user_id is None:
                    logger.warning("Token missing user ID")
                    raise credentials_exception
            except JWTError:
                logger.warning("JWT decode error")
                raise credentials_exception

            # Get user from database
            with get_enhanced_session() as session:
                # Ensure all required attributes are loaded before session closes
                from sqlmodel import select
                statement = select(User).where(User.id == user_id)
                result = session.exec(statement)
                user = result.first()

                if user is None:
                    logger.warning(f"User not found: {user_id}")
                    raise credentials_exception
                if not user.is_active:
                    logger.warning(f"Inactive user attempted access: {user_id}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Inactive user",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                # Ensure the user object is fully loaded by accessing its attributes
                _ = user.id  # Force loading of the id attribute
                _ = user.email  # Force loading of other important attributes
                return user
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Get current user error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during authentication"
            )

    def handle_auth_error(self, error: ValidationError) -> HTTPException:
        """Convert validation errors to appropriate HTTP exceptions."""
        error_map = {
            AuthError.INVALID_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
            AuthError.USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
            AuthError.USER_INACTIVE: status.HTTP_401_UNAUTHORIZED,
            AuthError.TOKEN_EXPIRED: status.HTTP_401_UNAUTHORIZED,
            AuthError.TOKEN_INVALID: status.HTTP_401_UNAUTHORIZED,
            AuthError.PASSWORD_WEAK: status.HTTP_400_BAD_REQUEST,
            AuthError.EMAIL_INVALID: status.HTTP_400_BAD_REQUEST,
            AuthError.USER_EXISTS: status.HTTP_409_CONFLICT,
            AuthError.DATABASE_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
            AuthError.RATE_LIMIT_EXCEEDED: status.HTTP_429_TOO_MANY_REQUESTS,
        }

        status_code = error_map.get(error.error_type, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return HTTPException(
            status_code=status_code,
            detail=error.message
        )


# Global instance
auth_config = AuthConfig()


# Convenience functions for backward compatibility
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Wrapper for password verification."""
    return auth_config.verify_password(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Wrapper for password hashing."""
    return auth_config.get_password_hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Wrapper for access token creation."""
    return auth_config.create_access_token(data, expires_delta)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Wrapper for refresh token creation."""
    return auth_config.create_refresh_token(data, expires_delta)


def verify_token(token: str) -> Optional[dict]:
    """Wrapper for token verification."""
    return auth_config.verify_token(token)


def get_current_user(token: str = Depends(auth_config.oauth2_scheme)):
    """Wrapper for getting current user with comprehensive error handling."""
    try:
        logger.info("Attempting to get current user from token")
        user = auth_config.get_current_user(token)
        logger.info(f"Successfully retrieved user: {user.id if user else 'None'}")
        return user
    except HTTPException:
        logger.error("HTTPException in get_current_user")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )


def get_current_user_id(token: str = Depends(auth_config.oauth2_scheme)) -> str:
    """Dependency to get just the current user ID as a string to avoid detached instance issues."""
    try:
        logger.info("Attempting to get current user ID from token")
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            logger.warning("Token missing user ID in get_current_user_id")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successfully retrieved user ID: {user_id}")
        return user_id
    except JWTError as e:
        logger.error(f"JWT decode error in get_current_user_id: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user_id: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )


def validate_email(email: str) -> bool:
    """Wrapper for email validation."""
    return auth_config.validate_email(email)


def validate_password(password: str) -> tuple[bool, str]:
    """Wrapper for password validation."""
    return auth_config.validate_password(password)