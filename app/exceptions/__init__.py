"""
Custom exceptions module for the FastAPI application.

This module provides a collection of custom HTTP exceptions
for consistent error handling across the application.
"""

from .not_found import NotFoundException
from .validation_error import ValidationError
from .unauthorized_error import UnauthorizedError
from .conflict_error import ConflictError


__all__ = ["NotFoundException", "ValidationError", "UnauthorizedError", "ConflictError"]
