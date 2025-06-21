"""
Base exception module for custom HTTP exceptions.

This module provides a base class for all custom HTTP exceptions
used throughout the application, ensuring consistent error handling
and response formatting.
"""

from fastapi import HTTPException
from typing import Optional, Dict, Any


class BaseException(HTTPException):
    """
    Base exception class for custom HTTP exceptions.

    This class extends FastAPI's HTTPException to provide consistent
    error handling across the application with additional features
    like error codes and structured error responses.

    Attributes:
        status_code: HTTP status code
        detail: Error message
        error_code: Application-specific error code
        extra_data: Additional error data
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the base exception.

        Args:
            status_code: HTTP status code
            detail: Error message
            error_code: Application-specific error code
            extra_data: Additional error data
        """
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.extra_data = extra_data or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary format.

        Returns:
            Dictionary representation of the exception
        """
        return {
            "error": {
                "code": self.error_code,
                "message": self.detail,
                "status_code": self.status_code,
                **self.extra_data,
            }
        }
