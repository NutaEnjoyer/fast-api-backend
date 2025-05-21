from fastapi import APIRouter

from app.api.task.task_router import router as task_router


routers = APIRouter(prefix="/api")

router_list = [
    task_router,
]

for router in router_list:
    routers.include_router(router)