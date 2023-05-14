from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.router import routers as v1_router
from app.core.config import configs
from app.core.container import Container
from app.core.exception import CustomHttpException


def create_app():
    _app = FastAPI(
        title=configs.PROJECT_NAME,
        docs_url=f"{configs.API_PREFIX}/docs",
        redoc_url=f"{configs.API_PREFIX}/redoc",
        openapi_url=f"{configs.API_PREFIX}/openapi.json",
        version="0.0.1",
    )

    # set db and container
    container = Container()
    _app.container = container
    _app.db = container.db()

    # set cors
    if configs.BACKEND_CORS_ORIGINS:
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @_app.exception_handler(CustomHttpException)
    async def http_exception_handler(
        request: Request,  # Don't remove it because it is used internally.
        exc: CustomHttpException,
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"title": exc.title, "description": exc.description})

    # set routes
    @_app.get(f"{configs.API_PREFIX}/healthcheck", status_code=status.HTTP_200_OK)
    def healthcheck():
        return {"status": "OK"}

    @_app.get("/", status_code=status.HTTP_200_OK)
    def root():
        return {"status": "OK"}

    _app.include_router(v1_router, prefix=configs.API_V1_PREFIX)
    logger.info(f"app created. Its ENV_NAME: {configs.ENV}")
    return _app


app = create_app()
