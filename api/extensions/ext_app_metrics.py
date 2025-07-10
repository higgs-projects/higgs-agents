import json
import os
import threading

from fastapi import Request, Response

from configs import higgs_config
from higgs_app import HiggsApp


def init_app(app: HiggsApp):
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        response: Response = await call_next(request)
        """Add Version headers to the response."""
        response.headers["X-Version"] = higgs_config.CURRENT_VERSION
        response.headers["X-Env"] = higgs_config.DEPLOY_ENV
        return response

    @app.get("/health")
    async def health():
        return Response(
            json.dumps({"pid": os.getpid(), "status": "ok", "version": higgs_config.CURRENT_VERSION}),
            status_code=200,
            media_type="application/json",
        )

    @app.get("/threads")
    async def threads():
        num_threads = threading.active_count()
        threads = threading.enumerate()

        thread_list = []
        for thread in threads:
            thread_name = thread.name
            thread_id = thread.ident
            is_alive = thread.is_alive()

            thread_list.append(
                {
                    "name": thread_name,
                    "id": thread_id,
                    "is_alive": is_alive,
                }
            )

        return Response(
            json.dumps(
                {
                    "pid": os.getpid(),
                    "thread_num": num_threads,
                    "threads": thread_list,
                }
            ),
            status_code=200,
            media_type="application/json",
        )

    @app.get("/db-pool-stat")
    async def pool_stat():
        from models.engine import engine

        return Response(
            json.dumps(
                {
                    "pid": os.getpid(),
                    "pool_size": engine.pool.size(),  # type: ignore
                    "checked_in_connections": engine.pool.checkedin(),  # type: ignore
                    "checked_out_connections": engine.pool.checkedout(),  # type: ignore
                    "overflow_connections": engine.pool.overflow(),  # type: ignore
                    "connection_timeout": engine.pool.timeout(),  # type: ignore
                    "recycle_time": engine.pool._recycle,  # type: ignore
                }
            ),
            status_code=200,
            media_type="application/json",
        )
