from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import redis.asyncio as redis

from app.core.configs import Config


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.limit = int(Config.get_env("ANTI_DDOS_RATE_LIMIT"))
        self.window = int(Config.get_env("ANTI_DDOS_RATE_WINDOW"))
        self.redis = redis.from_url("redis://localhost", decode_responses=True)

    async def dispatch(self, request: Request, call_next: Callable):
        ip = request.client.host
        path = request.url.path
        key = f"rate_limit:{ip}:{path}"

        print(key)

        try:
            current = await self.redis.get(key)
            if current is None:
                await self.redis.set(key, 1, ex=self.window)
            elif int(current) < self.limit:
                await self.redis.incr(key)
            else:
                ttl = await self.redis.ttl(key)
                return JSONResponse(
                    status_code=429,
                    content={"detail": f"Rate limit exceeded. Try again in {ttl} seconds."}
                )
        except Exception as e:
            print("Rate limiting error:", e)

        response = await call_next(request)
        return response