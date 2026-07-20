from fastapi import FastAPI

from app.config import settings
from app.api.router import router

app = FastAPI(
    title="QAshboard",
    openapi_url=f"{settings.API_V1}/openapi.json",
    generate_unique_id_function=lambda route: route.name,
)

app.include_router(router, prefix=settings.API_V1)
