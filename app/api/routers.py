"""
API routers configuration module.

This module centralizes all API router registrations and provides
a unified entry point for all application endpoints with proper
organization and documentation.
"""

from fastapi import APIRouter

from app.api.task.task_router import router as task_router
from app.api.auth.auth_router import router as auth_router
from app.api.user.user_router import router as user_router
from app.api.pomodoro.pomodoro_router import router as pomodoro_router


# Main API router with global prefix
routers = APIRouter(
    prefix="/api",
    tags=["API"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)

# List of all application routers
router_list = [
    auth_router,  # Authentication endpoints (/api/auth/*)
    user_router,  # User management endpoints (/api/user/*)
    task_router,  # Task management endpoints (/api/task/*)
    pomodoro_router,  # Pomodoro session endpoints (/api/pomodoro/*)
]

# Register all routers with the main API router
for router in router_list:
    routers.include_router(router)


def get_api_router() -> APIRouter:
    """
    Get the main API router with all registered endpoints.

    Returns:
        APIRouter: The main API router containing all application endpoints

    Example:
        ```python
        from app.api.routers import get_api_router

        app = FastAPI()
        app.include_router(get_api_router())
        ```
    """
    return routers
