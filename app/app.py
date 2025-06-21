"""
FastAPI application main module.

This module initializes the FastAPI application with all necessary
components including routers, middleware, database setup, and
lifespan management.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routers import get_api_router
from app.core.database import create_tables
from app.middlewares.rate_limiter import RateLimiterMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events for the FastAPI application.
    Creates database tables on startup and performs cleanup on shutdown.

    Args:
        app: FastAPI application instance
    """
    # Startup: Create database tables
    await create_tables()
    yield
    # Shutdown: Cleanup operations (if needed)
    # await cleanup_resources()


# Get the main API router with all endpoints
router = get_api_router()

# Create FastAPI application with metadata
app = FastAPI(
    title="Pomodoro Task Manager API",
    description="A comprehensive API for managing tasks and pomodoro sessions",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include all API routes
app.include_router(router)

# Add rate limiting middleware
app.add_middleware(RateLimiterMiddleware)


@app.get("/", tags=["Health"])
def read_root():
    """
    Health check endpoint.

    Returns a simple message to verify the API is running.

    Returns:
        dict: Simple health check response
    """
    return {"message": "Pomodoro Task Manager API is running", "status": "healthy"}
