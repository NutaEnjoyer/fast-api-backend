"""
Authentication DTO (Data Transfer Object) module.

This module provides DTOs for authentication operations including
login, registration, and token management with proper validation.
"""

from pydantic import EmailStr

from app.dto.base_dto import BaseModelDto


class AuthDto(BaseModelDto):
    """
    DTO for user authentication operations.

    Contains credentials required for user authentication
    with proper email validation.
    """

    email: EmailStr
    password: str


class AuthResponseDto(BaseModelDto):
    """
    DTO for authentication response.

    Contains access token for successful authentication operations.
    """

    access_token: str
