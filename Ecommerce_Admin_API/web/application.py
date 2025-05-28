from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from Ecommerce_Admin_API.log import configure_logging
from Ecommerce_Admin_API.web.api.router import api_router
from Ecommerce_Admin_API.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="Ecommerce_Admin_API",
        version=metadata.version("Ecommerce_Admin_API"),
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
