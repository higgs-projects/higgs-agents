from fastapi import APIRouter

from .demo import router as index_router
from .playgroud import playground_router

service_api_router = APIRouter(prefix="/v1")
service_api_router.include_router(playground_router)
service_api_router.include_router(index_router)
