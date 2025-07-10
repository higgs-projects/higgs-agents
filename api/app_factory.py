import logging
import time
from contextlib import asynccontextmanager

from configs import higgs_config
from contexts.wrapper import RecyclableContextVar
from higgs_app import HiggsApp


# ----------------------------
# Application Factory Function
# ----------------------------
def create_fastapi_app_with_configs() -> HiggsApp:
    """
    create a raw flask app
    with configs loaded from .env file
    """

    @asynccontextmanager
    async def lifespan(app: HiggsApp):
        # add an unique identifier to each request
        RecyclableContextVar.increment_thread_recycles()
        yield

    higgs_app = HiggsApp(
        title="Higgs Agents OpenAPI", debug=higgs_config.DEBUG, version=higgs_config.CURRENT_VERSION, lifespan=lifespan
    )

    return higgs_app


def create_app() -> HiggsApp:
    start_time = time.perf_counter()
    app = create_fastapi_app_with_configs()
    initialize_extensions(app)
    end_time = time.perf_counter()
    if higgs_config.DEBUG:
        logging.info(f"Finished create_app ({round((end_time - start_time) * 1000, 2)} ms)")
    return app


def initialize_extensions(app: HiggsApp):
    from extensions import (
        ext_app_metrics,
        ext_compress,
        ext_exception,
        ext_logging,
        ext_migrate,
        ext_router,
        ext_timezone,
        ext_warnings,
    )

    extensions = [
        ext_logging,
        ext_app_metrics,
        ext_compress,
        ext_exception,
        ext_router,
        ext_migrate,
        ext_timezone,
        ext_warnings,
    ]
    for ext in extensions:
        short_name = ext.__name__.split(".")[-1]
        is_enabled = ext.is_enabled() if hasattr(ext, "is_enabled") else True
        if not is_enabled:
            if higgs_config.DEBUG:
                logging.info(f"Skipped {short_name}")
            continue

        start_time = time.perf_counter()
        ext.init_app(app)
        end_time = time.perf_counter()
        if higgs_config.DEBUG:
            logging.info(f"Loaded {short_name} ({round((end_time - start_time) * 1000, 2)} ms)")


def create_migrations_app():
    app = create_fastapi_app_with_configs()
    from extensions import ext_database, ext_migrate

    # Initialize only required extensions
    ext_database.init_app(app)
    ext_migrate.init_app(app)

    return app
