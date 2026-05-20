"""
This file defines custom, domain-specific exceptions for the application.
By using these custom exceptions, the Service layer can signal specific errors 
(like a DuplicateEmailError) without needing to know how the error will be 
presented to the user. The Global Error Handler later catches these exceptions 
and converts them into standard HTTP error responses.
"""

class AppException(Exception):
    """Base class for all custom application exceptions."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class NotFoundError(AppException):
    """Raised when an entity is not found in the database."""
    pass

class DuplicateEmailError(AppException):
    """Raised when attempting to create or update an employee with an email that is already taken."""
    pass

class ValidationException(AppException):
    """Raised when general business logic validation fails."""
    pass
