import os
from typing import Any, Dict
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()


class Config:
    @classmethod
    def get_env(cls, key: str, default: str | None = None) -> str | None:
        return os.getenv(key, default)


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

    # Database URL
    database_url = Config.get_env("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    config["database_url"] = database_url

    # Redis URL
    redis_url = Config.get_env("REDIS_URL")
    if not redis_url:
        raise ValueError("REDIS_URL environment variable is required")
    config["redis_url"] = redis_url

    # Anti-DDOS configuration
    try:
        config["anti_ddos_rate_limit"] = int(
            Config.get_env("ANTI_DDOS_RATE_LIMIT") or "50"
        )
        config["anti_ddos_rate_window"] = int(
            Config.get_env("ANTI_DDOS_RATE_WINDOW") or "60"
        )
    except ValueError as e:
        raise ValueError(f"Invalid anti-ddos configuration: {e}")

    # Debug mode
    debug = Config.get_env("DEBUG")

    if debug:
        if debug.lower() == "true":
            config["debug"] = True
        else:
            config["debug"] = False
    else:
        config["debug"] = False

    return config


# Load configuration on module import
try:
    SECURITY_CONFIG = _load_security_config()
    JWT_SECRET_KEY: str = SECURITY_CONFIG["jwt_secret_key"]
    ALGORITHM: str = SECURITY_CONFIG["algorithm"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = SECURITY_CONFIG["access_token_expire_minutes"]
    REFRESH_TOKEN_EXPIRE_MINUTES: int = (
        SECURITY_CONFIG["refresh_token_expire_days"] * 24 * 60
    )
    DATABASE_URL: str = SECURITY_CONFIG["database_url"]
    REDIS_URL: str = SECURITY_CONFIG["redis_url"]
    ANTI_DDOS_RATE_LIMIT: int = SECURITY_CONFIG["anti_ddos_rate_limit"]
    ANTI_DDOS_RATE_WINDOW: int = SECURITY_CONFIG["anti_ddos_rate_window"]
    DEBUG: bool = SECURITY_CONFIG["debug"]
except Exception as e:
    logger.error(f"Failed to load security configuration: {e}")
    raise
