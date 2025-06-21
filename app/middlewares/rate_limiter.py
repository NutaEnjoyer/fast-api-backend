"""
Rate limiter middleware module for DDoS protection.

This module contains the RateLimiterMiddleware class which provides
rate limiting functionality to protect the API from abuse and DDoS attacks.
"""

import logging
from typing import Callable, Optional
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import redis.asyncio as redis

from app.core.configs import ANTI_DDOS_RATE_LIMIT, ANTI_DDOS_RATE_WINDOW, REDIS_URL

# Setup logging
logger = logging.getLogger(__name__)


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Rate limiter middleware for DDoS protection.

    This middleware implements rate limiting based on IP address and request path.
    It uses Redis to store request counts and provides protection against
    abuse and DDoS attacks.

    Attributes:
        limit: Maximum number of requests allowed per window
        window: Time window in seconds for rate limiting
        redis: Redis client for storing rate limit data
    """

    def __init__(self, app):
        """
        Initialize the rate limiter middleware.

        Args:
            app: The FastAPI application instance
        """
        super().__init__(app)
        self.limit = ANTI_DDOS_RATE_LIMIT
        self.window = ANTI_DDOS_RATE_WINDOW
        self.redis = redis.from_url(REDIS_URL, decode_responses=True)

    def _get_client_ip(self, request: Request) -> str:
        """
        Extract client IP address from request.

        Handles various scenarios including proxy headers and missing client info.

        Args:
            request: FastAPI request object

        Returns:
            Client IP address as string
        """
        # Check for forwarded IP from proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # Check for real IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fallback to client host
        if request.client is None:
            return "unknown"

        return request.client.host

    def _create_rate_limit_key(self, ip: str, path: str) -> str:
        """
        Create Redis key for rate limiting.

        Args:
            ip: Client IP address
            path: Request path

        Returns:
            Redis key string
        """
        return f"rate_limit:{ip}:{path}"

    async def _check_rate_limit(self, key: str) -> Optional[int]:
        """
        Check if request is within rate limit.

        Args:
            key: Redis key for rate limiting

        Returns:
            TTL in seconds if rate limit exceeded, None otherwise

        Raises:
            Exception: If Redis operation fails
        """
        current = await self.redis.get(key)

        if current is None:
            # First request, set initial count
            await self.redis.set(key, 1, ex=self.window)
            return None
        elif int(current) < self.limit:
            # Within limit, increment counter
            await self.redis.incr(key)
            return None
        else:
            # Rate limit exceeded, return TTL
            return await self.redis.ttl(key)

    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process incoming request and apply rate limiting.

        Args:
            request: FastAPI request object
            call_next: Next middleware or endpoint handler

        Returns:
            FastAPI response object
        """
        # Skip rate limiting for unknown clients
        ip = self._get_client_ip(request)
        if ip == "unknown":
            logger.warning("Rate limiting skipped for unknown client")
            return await call_next(request)

        path = request.url.path
        key = self._create_rate_limit_key(ip, path)

        logger.debug(f"Rate limiting check for {ip} on {path}")

        try:
            ttl = await self._check_rate_limit(key)

            if ttl is not None:
                logger.warning(f"Rate limit exceeded for {ip} on {path}, TTL: {ttl}s")
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"Rate limit exceeded. Try again in {ttl} seconds.",
                        "retry_after": ttl,
                    },
                )

        except Exception as e:
            logger.error(f"Rate limiting error for {ip}: {e}")
            # Continue processing request if rate limiting fails
            # This prevents rate limiting from breaking the application

        response = await call_next(request)
        return response
