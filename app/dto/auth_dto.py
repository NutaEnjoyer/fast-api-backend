"""
Authentication DTO (Data Transfer Object) module.

This module provides DTOs for authentication operations including
login, registration, and token management with proper validation.
"""

from pydantic import BaseModel, EmailStr


class AuthDto(BaseModel):
    """
    DTO for user authentication operations.

    Contains credentials required for user authentication
    with proper email validation.
    """

    email: EmailStr
    password: str


class AuthResponseDto(BaseModel):
    """
    DTO for authentication response.

    Contains access token for successful authentication operations.
    """

    access_token: str
