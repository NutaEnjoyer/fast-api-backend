from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from datetime import datetime

from contextlib import asynccontextmanager  

from api.routers import routers
from database import create_tables, delete_tables
from dto.task_dto import CreateTaskDto, TaskDto


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start")
    await create_tables()
    print("created")
    yield
    await delete_tables()


app = FastAPI(lifespan=lifespan)
app.include_router(routers)


@app.get("/")
def read_root():
    return {"Hello": "World"}

