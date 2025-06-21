"""
Response DTO (Data Transfer Object) module.

This module provides base response DTOs for API operations
with standardized success/error handling and metadata.
"""

from pydantic import BaseModel


class ResponseDto(BaseModel):
    """
    Base response DTO for API operations.

    Provides standardized response structure with success status
    for all API endpoints.
    """

    ok: bool = True
