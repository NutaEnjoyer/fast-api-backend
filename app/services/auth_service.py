"""
Authentication service module for user authentication operations.

This module contains the AuthService class which handles business logic
for user authentication, including registration, login, logout, and
token management. It provides secure authentication mechanisms with
JWT tokens and refresh token cookies.
"""

from fastapi import Request, Response, HTTPException
from app.dto.auth_dto import AuthDto, AuthResponseDto
from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.core.security import (
    decode_token,
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    REFRESH_TOKEN_COOKIE_NAME,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from app.core.configs import DEBUG
from exceptions import UnauthorizedError, ConflictError, NotFoundException


class AuthService(BaseService):
    """
    Service class for authentication operations.

    This class handles business logic for user authentication, including
    user registration, login, logout, and token management. It provides
    secure authentication mechanisms with JWT tokens and refresh token
    cookies for persistent sessions.

    The AuthService manages the complete authentication flow, including
    password hashing, token generation, cookie management, and user
    validation.
    """

    def __init__(self, user_repository: UserRepository = UserRepository()):
        """
        Initialize the authentication service.

        Args:
            user_repository: Repository for user operations
        """
        self.user_repository = user_repository

    def _set_refresh_token_cookie(self, response: Response, refresh_token: str):
        """
        Set refresh token in HTTP-only cookie.

        Args:
            response: FastAPI response object
            refresh_token: JWT refresh token to set in cookie
        """
        response.set_cookie(
            key=REFRESH_TOKEN_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            secure=not DEBUG,  # True for production
            samesite="lax",
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )

    def _remove_refresh_token_cookie(self, response: Response):
        """
        Remove refresh token cookie.

        Args:
            response: FastAPI response object
        """
        response.delete_cookie(REFRESH_TOKEN_COOKIE_NAME)

    async def _get_new_tokens(self, _refresh_token: str) -> tuple[str, str]:
        """
        Generate new access and refresh tokens from existing refresh token.

        Args:
            _refresh_token: Existing refresh token

        Returns:
            Tuple of (access_token, refresh_token)

        Raises:
            UnauthorizedError: If refresh token is invalid or user not found
        """
        result = decode_token(_refresh_token)
        if not result:
            raise UnauthorizedError(detail="Invalid refresh token")

        user_id = result.get("id")
        if not user_id:
            raise UnauthorizedError(detail="Invalid token payload")

        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundException(
                detail="User not found", resource_type="User", resource_id=user_id
            )

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return access_token, refresh_token

    async def register(self, data: AuthDto, response: Response) -> AuthResponseDto:
        """
        Register a new user.

        Args:
            data: Authentication data containing email and password
            response: FastAPI response object for setting cookies

        Returns:
            Authentication response with access token

        Raises:
            ConflictError: If email is already registered
            ValidationError: If input data is invalid
        """
        existing_user = await self.user_repository.find_by_email(data.email)

        if existing_user:
            raise ConflictError(detail="Email already registered")

        hashed_password = hash_password(data.password)
        data.password = hashed_password
        user = await self.user_repository.create(data)

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        self._set_refresh_token_cookie(response, refresh_token)

        return AuthResponseDto(access_token=access_token)

    async def login(self, data: AuthDto, response: Response) -> AuthResponseDto:
        """
        Authenticate existing user.

        Args:
            data: Authentication data containing email and password
            response: FastAPI response object for setting cookies

        Returns:
            Authentication response with access token

        Raises:
            NotFoundException: If user with email doesn't exist
            UnauthorizedError: If password is incorrect
        """
        user = await self.user_repository.find_by_email(data.email)

        if not user:
            raise NotFoundException(
                detail="User with this Email does not exist",
                resource_type="User",
                resource_id=data.email,
            )

        if not verify_password(data.password, user.password):
            raise UnauthorizedError(detail="Incorrect password")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        self._set_refresh_token_cookie(response, refresh_token)

        return AuthResponseDto(access_token=access_token)

    async def logout(self, response: Response) -> None:
        """
        Logout user by removing refresh token cookie.

        Args:
            response: FastAPI response object for removing cookies
        """
        self._remove_refresh_token_cookie(response)

    async def login_access(
        self, request: Request, response: Response
    ) -> AuthResponseDto:
        """
        Refresh access token using refresh token from cookies.

        Args:
            request: FastAPI request object containing cookies
            response: FastAPI response object for setting new cookies

        Returns:
            Authentication response with new access token

        Raises:
            UnauthorizedError: If refresh token is missing or invalid
        """
        refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE_NAME)
        if not refresh_token:
            self._remove_refresh_token_cookie(response)
            raise UnauthorizedError(detail="Refresh token not found")

        access_token, refresh_token = await self._get_new_tokens(refresh_token)
        self._set_refresh_token_cookie(response, refresh_token)

        return AuthResponseDto(access_token=access_token)
