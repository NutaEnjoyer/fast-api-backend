import bcrypt
import logging
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from app.core.configs import Config

# Logging setup
logger = logging.getLogger(__name__)

# Configuration validation and loading
def _load_security_config() -> Dict[str, Any]:
    """Loads and validates security configuration"""
    config = {}
    
    # JWT Secret Key
    jwt_secret = Config.get_env("JWT_SECRET_KEY")
    if not jwt_secret:
        raise ValueError("JWT_SECRET_KEY environment variable is required")
    config["jwt_secret_key"] = jwt_secret
    
    # Algorithm
    config["algorithm"] = Config.get_env("ALGORITHM") or "HS256"
    
    # Token expiration
    try:
        config["access_token_expire_minutes"] = int(
            Config.get_env("ACCESS_TOKEN_EXPIRE_MINUTES") or "15"
        )
        config["refresh_token_expire_days"] = int(
            Config.get_env("REFRESH_TOKEN_EXPIRE_DAYS") or "7"
        )
    except ValueError as e:
        raise ValueError(f"Invalid token expiration configuration: {e}")
    
    database_url = Config.get_env("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    config["database_url"] = database_url

    return config

# Load configuration on module import
try:
    SECURITY_CONFIG = _load_security_config()
    JWT_SECRET_KEY: str = SECURITY_CONFIG["jwt_secret_key"]
    ALGORITHM: str = SECURITY_CONFIG["algorithm"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = SECURITY_CONFIG["access_token_expire_minutes"]
    REFRESH_TOKEN_EXPIRE_MINUTES: int = SECURITY_CONFIG["refresh_token_expire_days"] * 24 * 60
    DATABASE_URL: str = SECURITY_CONFIG["database_url"]
except Exception as e:
    logger.error(f"Failed to load security configuration: {e}")
    raise

# Constants
ACCESS_TOKEN_COOKIE_NAME: str = 'access_token'
REFRESH_TOKEN_COOKIE_NAME: str = 'refresh_token'


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
    return create_token({"id": user_id}, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))


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
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode('utf-8')
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
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logger.error(f"Failed to verify password: {e}")
        return False
