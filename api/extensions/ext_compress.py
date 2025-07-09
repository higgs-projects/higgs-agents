from starlette.middleware.gzip import GZipMiddleware

from configs import higgs_config
from higgs_app import HiggsApp


def is_enabled() -> bool:
    return higgs_config.API_COMPRESSION_ENABLED


def init_app(app: HiggsApp):
    # 添加 GZip 中间件到 FastAPI 应用中
    app.add_middleware(GZipMiddleware, minimum_size=1000)
