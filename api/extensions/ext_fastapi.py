import logging
import re
import sys
from http import HTTPStatus
from typing import Any

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from higgs_app import HiggsApp

# 配置日志记录器
logger = logging.getLogger(__name__)


def init_app(app: HiggsApp):
    from fastapi.middleware.cors import CORSMiddleware

    from controllers.service_api import service_api_router

    # 添加路由
    app.include_router(service_api_router, prefix="/v1")

    # 设置cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 处理全局异常
    @app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, e: Exception):
        headers = request.headers

        if isinstance(e, HTTPException):
            status_code = e.status_code
            default_data = {
                "code": re.sub(r"(?<!^)(?=[A-Z])", "_", type(e).__name__).lower(),
                "message": getattr(e, "detail", HTTPStatus(status_code).phrase),
                "status": status_code,
            }

            if (
                default_data["message"]
                and default_data["message"] == "Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)"
            ):
                default_data["message"] = "Invalid JSON payload received or JSON payload is empty."

        elif isinstance(e, ValueError):
            status_code = 400
            default_data = {
                "code": "invalid_param",
                "message": str(e),
                "status": status_code,
            }
        else:
            status_code = 500
            default_data = {
                "message": HTTPStatus(status_code).phrase,
            }

        data = getattr(e, "data", default_data)

        # record the exception in the logs when we have a server error of status code: 500
        if status_code and status_code >= 500:
            exc_info: Any = sys.exc_info()
            if exc_info[1] is None:
                exc_info = None
            logger.error(exc_info)

        if status_code == 406:
            # if we are handling NotAcceptable (406), make sure that
            # make_response uses a representation we support as the
            # default mediatype (so that make_response doesn't throw
            # another NotAcceptable error).
            accept_header = headers.get("accept", "*/*")
            fallback_mediatype = "application/json" if "application/json" in accept_header else "text/plain"
            data = {"code": "not_acceptable", "message": data.get("message")}
            resp = JSONResponse(data, status_code, headers, media_type=fallback_mediatype)

        elif status_code == 400:
            if isinstance(data.get("message"), dict):
                param_key, param_value = list(data.get("message", {}).items())[0]
                data = {"code": "invalid_param", "message": param_value, "params": param_key}
            else:
                if "code" not in data:
                    data["code"] = "unknown"

            resp = JSONResponse(data, status_code, headers)
        else:
            if "code" not in data:
                data["code"] = "unknown"

            resp = JSONResponse(data, status_code, headers)

        if status_code == 401:
            resp = JSONResponse(
                content={"message": data.get("message")},
                status_code=status_code,
                headers={"WWW-Authenticate": "Bearer realm='fastapi_realm'"},
            )
        return resp
