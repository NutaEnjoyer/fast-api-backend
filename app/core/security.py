import bcrypt
import logging
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from app.core.configs import (
    JWT_SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)

# Logging setup
logger = logging.getLogger(__name__)

# Constants
ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"


def create_token(data: Dict[str, Any], _timedelta: timedelta) -> str:
    """
    Creates JWT token with specified data and lifetime

    Args:
        data: Data to include in the token
        _timedelta: Token lifetime

    Returns:
        Encoded JWT token

    Raises:
        Exception: When token creation fails
    """
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + _timedelta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.error(f"Failed to create token: {e}")
        raise


def create_access_token(user_id: str) -> str:
    """
    Creates access token for user

    Args:
        user_id: User ID

    Returns:
        Access token
    """
    return create_token({"id": user_id}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(user_id: str) -> str:
    """
    Creates refresh token for user

    Args:
        user_id: User ID

    Returns:
        Refresh token
    """
    return create_token(
        {"id": user_id}, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes JWT token

    Args:
        token: JWT token to decode

    Returns:
        Decoded token data or None on error
    """
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        logger.warning(f"Failed to decode token: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {e}")
        return None


def hash_password(password: str) -> str:
    """
    Hashes password using bcrypt

    Args:
        password: Password to hash

    Returns:
        Hashed password

    Raises:
        ValueError: When password is empty
    """
    if not password:
        raise ValueError("Password cannot be empty")

    try:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode("utf-8")
    except Exception as e:
        logger.error(f"Failed to hash password: {e}")
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies password against its hash

    Args:
        plain_password: Password in plain text
        hashed_password: Hashed password

    Returns:
        True if passwords match, False otherwise
    """
    if not plain_password or not hashed_password:
        return False

    try:
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logger.error(f"Failed to verify password: {e}")
        return False
