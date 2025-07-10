from higgs_app import HiggsApp


def init_app(app: HiggsApp):
    from fastapi.middleware.cors import CORSMiddleware

    from controllers.service_api import service_api_router

    # 添加路由
    app.include_router(service_api_router)

    # 设置cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://app.agno.com", "http://localhost", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
