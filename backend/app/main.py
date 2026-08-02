from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings
from app.api.router import router

@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.BUILD_LOGS_TEMP_PATH.mkdir(exist_ok=True, parents=True)
    yield

app = FastAPI(
    title="QAshboard",
    openapi_url=f"{settings.API_V1}/openapi.json",
    generate_unique_id_function=lambda route: route.name,
    lifespan=lifespan
)

app.include_router(router, prefix=settings.API_V1)
