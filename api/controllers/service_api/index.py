from configs import higgs_config
from controllers.service_api import service_api_router


@service_api_router.get("/")
async def index():
    return {
        "welcome": "Higgs Agents OpenAPI",
        "api_version": "v1",
        "server_version": higgs_config.CURRENT_VERSION,
    }
