from fastapi import APIRouter

from app.api.task.task_router import router as task_router
from app.api.auth.auth_router import router as auth_router
from app.api.user.user_router import router as user_router


routers = APIRouter(prefix="/api")

router_list = [
    auth_router,
    user_router,
    task_router,
]

for router in router_list:
    routers.include_router(router)
