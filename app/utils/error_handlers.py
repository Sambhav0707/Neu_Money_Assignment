"""
This file contains Global Error Handlers.
It intercepts custom exceptions thrown by the Service layer (like NotFoundError) 
and translates them into standardized, predictable HTTP JSON responses.
This prevents the application from crashing and hides internal stack traces from users.
"""

from flask import Flask
from app.exceptions.custom_exceptions import (
    NotFoundError,
    DuplicateEmailError,
    ValidationException,
    AppException
)
from app.utils.response import error_response

def register_error_handlers(app: Flask):
    """
    Registers global error handlers for the Flask application.
    Intercepts domain exceptions and maps them to HTTP status codes.
    """

    @app.errorhandler(ValidationException)
    def handle_validation_error(error: ValidationException):
        return error_response(message=error.message, status_code=400)

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error: NotFoundError):
        return error_response(message=error.message, status_code=404)

    @app.errorhandler(DuplicateEmailError)
    def handle_duplicate_email_error(error: DuplicateEmailError):
        return error_response(message=error.message, status_code=409)

    @app.errorhandler(AppException)
    def handle_app_exception(error: AppException):
        return error_response(message=error.message, status_code=400)

    @app.errorhandler(Exception)
    def handle_generic_exception(error: Exception):
        # In a production environment, log the raw exception here
        return error_response(message="An unexpected internal server error occurred.", status_code=500)
