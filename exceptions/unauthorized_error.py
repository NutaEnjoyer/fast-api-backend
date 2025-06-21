"""
Unauthorized error exception module.

This module provides the UnauthorizedError class for handling
401 Unauthorized errors related to authentication.
"""

from .base_exception import BaseException
from typing import Optional, Dict, Any


class UnauthorizedError(BaseException):
    """
    Exception raised when authentication fails.

    This exception is used to handle 401 Unauthorized errors
    related to missing or invalid authentication credentials.
    """

    def __init__(
        self,
        detail: str = "Authentication required",
        auth_type: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the unauthorized error exception.

        Args:
            detail: Error message
            auth_type: Type of authentication that failed (e.g., "JWT", "Basic")
            extra_data: Additional error data
        """
        extra = extra_data or {}
        if auth_type:
            extra["auth_type"] = auth_type

        super().__init__(
            status_code=401, detail=detail, error_code="UNAUTHORIZED", extra_data=extra
        )
