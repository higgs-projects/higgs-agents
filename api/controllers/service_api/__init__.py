from fastapi import APIRouter

from .demo import router as demo_router
from .playgroud import playground_router

service_api_router = APIRouter(prefix="/v1", dependencies=[])
service_api_router.include_router(playground_router)
service_api_router.include_router(demo_router)
