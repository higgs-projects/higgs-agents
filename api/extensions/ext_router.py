from higgs_app import HiggsApp


def init_app(app: HiggsApp):
    from agno.os import AgentOS
    from fastapi.middleware.cors import CORSMiddleware

    from agents import get_agents
    from controllers.service_api import service_api_router

    # 添加自定义路由
    app.include_router(service_api_router)

    # 添加AgentOS路由
    agent_os = AgentOS(
        description="Example app with custom routers",
        agents=get_agents(),
        fastapi_app=app,
    )
    agent_os.get_app()

    # 设置cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://os.agno.com", "http://localhost", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
