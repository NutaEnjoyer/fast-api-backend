"""
Not found exception module.

This module provides the NotFoundException class for handling
404 Not Found errors in a consistent way across the application.
"""

from .base_exception import BaseException
from typing import Optional, Dict, Any


class NotFoundException(BaseException):
    """
    Exception raised when a requested resource is not found.

    This exception is used to handle 404 Not Found errors with
    consistent formatting and additional context information.
    """

    def __init__(
        self,
        detail: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the not found exception.

        Args:
            detail: Error message
            resource_type: Type of resource that was not found (e.g., "User", "Task")
            resource_id: ID of the resource that was not found
            extra_data: Additional error data
        """
        error_code = "NOT_FOUND"
        if resource_type:
            error_code = f"{resource_type.upper()}_NOT_FOUND"

        extra = extra_data or {}
        if resource_type:
            extra["resource_type"] = resource_type
        if resource_id:
            extra["resource_id"] = resource_id

        super().__init__(
            status_code=404, detail=detail, error_code=error_code, extra_data=extra
        )
