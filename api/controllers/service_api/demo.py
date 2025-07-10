from fastapi import APIRouter

from configs import higgs_config

router = APIRouter(prefix="/demo", tags=["Demo"])


@router.get("/index")
async def index():
    return {
        "welcome": "Higgs Agents OpenAPI",
        "api_version": "v1",
        "server_version": higgs_config.CURRENT_VERSION,
    }
