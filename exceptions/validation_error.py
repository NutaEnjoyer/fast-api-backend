"""
Validation error exception module.

This module provides the ValidationError class for handling
400 Bad Request errors related to data validation.
"""

from .base_exception import BaseException
from typing import Optional, Dict, Any, List


class ValidationError(BaseException):
    """
    Exception raised when data validation fails.

    This exception is used to handle 400 Bad Request errors
    related to invalid input data with detailed validation
    information.
    """

    def __init__(
        self,
        detail: str,
        field_errors: Optional[List[Dict[str, Any]]] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the validation error exception.

        Args:
            detail: General error message
            field_errors: List of specific field validation errors
            extra_data: Additional error data
        """
        extra = extra_data or {}
        if field_errors:
            extra["field_errors"] = field_errors

        super().__init__(
            status_code=400,
            detail=detail,
            error_code="VALIDATION_ERROR",
            extra_data=extra,
        )
