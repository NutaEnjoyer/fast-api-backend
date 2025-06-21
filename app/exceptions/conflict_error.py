"""
Conflict error exception module.

This module provides the ConflictError class for handling
409 Conflict errors related to resource conflicts.
"""

from .base_exception import BaseException
from typing import Optional, Dict, Any


class ConflictError(BaseException):
    """
    Exception raised when a resource conflict occurs.

    This exception is used to handle 409 Conflict errors
    related to resource conflicts, such as duplicate emails,
    unique constraint violations, etc.
    """

    def __init__(
        self,
        detail: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        conflict_field: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the conflict error exception.

        Args:
            detail: Error message
            resource_type: Type of resource that caused conflict (e.g., "User", "Email")
            resource_id: ID or value of the conflicting resource
            conflict_field: Field that caused the conflict (e.g., "email", "username")
            extra_data: Additional error data
        """
        extra = extra_data or {}
        if resource_type:
            extra["resource_type"] = resource_type
        if resource_id:
            extra["resource_id"] = resource_id
        if conflict_field:
            extra["conflict_field"] = conflict_field

        super().__init__(
            status_code=409, detail=detail, error_code="CONFLICT", extra_data=extra
        )
