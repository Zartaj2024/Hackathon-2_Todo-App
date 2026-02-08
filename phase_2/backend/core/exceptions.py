"""
Custom exceptions for the Todo Web Application.
"""


class TodoException(Exception):
    """
    Base exception class for the Todo application.
    """
    def __init__(self, detail: str, status_code: int = 400, error_code: str = "GENERAL_ERROR"):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.detail)


class AuthenticationException(TodoException):
    """
    Exception raised for authentication-related errors.
    """
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            detail=detail,
            status_code=401,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationException(TodoException):
    """
    Exception raised for authorization-related errors.
    """
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(
            detail=detail,
            status_code=403,
            error_code="AUTHORIZATION_ERROR"
        )


class ResourceNotFoundException(TodoException):
    """
    Exception raised when a requested resource is not found.
    """
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            detail=detail,
            status_code=404,
            error_code="RESOURCE_NOT_FOUND"
        )


class ValidationError(TodoException):
    """
    Exception raised for validation-related errors.
    """
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            detail=detail,
            status_code=422,
            error_code="VALIDATION_ERROR"
        )


class DuplicateResourceException(TodoException):
    """
    Exception raised when attempting to create a duplicate resource.
    """
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            detail=detail,
            status_code=409,
            error_code="DUPLICATE_RESOURCE_ERROR"
        )


class InternalServerErrorException(TodoException):
    """
    Exception raised for internal server errors.
    """
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            detail=detail,
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR"
        )