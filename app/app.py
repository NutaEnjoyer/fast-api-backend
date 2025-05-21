from fastapi import FastAPI

from contextlib import asynccontextmanager  

from app.api.routers import routers
from app.core.database import create_tables, delete_tables
from app.dto.task_dto import CreateTaskDto, TaskDto
from middlewares.rate_limiter import RateLimiterMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    ...


app = FastAPI(lifespan=lifespan)
app.include_router(routers)

app.add_middleware(RateLimiterMiddleware)

@app.get("/")
def read_root():
    return {"Hello": "World"}

