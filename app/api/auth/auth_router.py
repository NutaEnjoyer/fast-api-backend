"""
Authentication API router module.

This module provides authentication-related API endpoints including
user registration, login, logout, and token management with proper
security measures and validation.
"""

from fastapi import APIRouter, Request, Response, Depends, status, HTTPException
from app.dto.auth_dto import AuthDto, AuthResponseDto
from app.services.auth_service import AuthService


# Authentication API router with prefix and tags
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
        409: {"description": "User already exists"},
    },
)


def get_auth_service() -> AuthService:
    """
    Dependency injection for AuthService.

    Creates and returns an AuthService instance for
    handling authentication operations.

    Returns:
        AuthService: Configured authentication service instance
    """
    return AuthService()


@router.post(
    "/register",
    response_model=AuthResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with email and password",
)
async def register(
    data: AuthDto,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponseDto:
    """
    Register a new user account.

    Creates a new user account with the provided credentials
    and returns an access token for immediate authentication.

    Args:
        data: User registration data (email and password)
        response: FastAPI response object for setting cookies
        auth_service: Authentication service dependency

    Returns:
        AuthResponseDto: Access token and user information

    Raises:
        HTTPException: If user already exists or registration fails
    """
    try:
        result: AuthResponseDto = await auth_service.register(data, response)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user",
        )


@router.post(
    "/login",
    response_model=AuthResponseDto,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate user with email and password",
)
async def login(
    data: AuthDto,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponseDto:
    """
    Authenticate user login.

    Validates user credentials and returns an access token
    for authenticated session management.

    Args:
        data: User login credentials (email and password)
        response: FastAPI response object for setting cookies
        auth_service: Authentication service dependency

    Returns:
        AuthResponseDto: Access token and user information

    Raises:
        HTTPException: If credentials are invalid or login fails
    """
    try:
        result: AuthResponseDto = await auth_service.login(data, response)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


@router.post(
    "/login/access-token",
    response_model=AuthResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Login with access token",
    description="Authenticate user using existing access token",
)
async def login_access_token(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponseDto:
    """
    Login using access token.

    Authenticates user using an existing access token
    from cookies or headers for session renewal.

    Args:
        request: FastAPI request object containing token
        response: FastAPI response object for setting cookies
        auth_service: Authentication service dependency

    Returns:
        AuthResponseDto: New access token and user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        result: AuthResponseDto = await auth_service.login_access(request, response)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="User logout",
    description="Logout user and invalidate session",
)
async def logout(
    response: Response, auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    """
    Logout user and invalidate session.

    Clears authentication cookies and invalidates the
    current user session for security purposes.

    Args:
        response: FastAPI response object for clearing cookies
        auth_service: Authentication service dependency

    Returns:
        dict: Confirmation of successful logout

    Raises:
        HTTPException: If logout operation fails
    """
    try:
        await auth_service.logout(response)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to logout"
        )
