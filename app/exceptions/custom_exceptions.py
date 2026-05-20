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
