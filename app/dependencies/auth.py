"""
Authentication dependencies module.

This module provides FastAPI dependencies for handling authentication
and user authorization in the application.
"""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_token
from app.exceptions import UnauthorizedError

# OAuth2 scheme configuration for token-based authentication
oauth2scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)


async def get_current_user(token: str = Depends(oauth2scheme)) -> str:
    """
    Get current authenticated user from JWT token.

    This dependency extracts and validates the JWT token from the request,
    decodes it to get user information, and returns the user ID.

    Args:
        token: JWT token from OAuth2PasswordBearer dependency

    Returns:
        str: User ID from the decoded token

    Raises:
        UnauthorizedError: If token is invalid, expired, or missing user ID

    Example:
        ```python
        @app.get("/protected")
        async def protected_route(user_id: str = Depends(get_current_user)):
            return {"message": f"Hello user {user_id}"}
        ```
    """
    # Decode and validate the JWT token
    payload = decode_token(token)
    if not payload:
        raise UnauthorizedError(detail="Invalid or expired token")

    # Extract user ID from token payload
    user_id = payload.get("id")
    if not user_id:
        raise UnauthorizedError(detail="Token missing user ID")

    return user_id
