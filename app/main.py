from fastapi import FastAPI, status
from app.core.config import config
from starlette.middleware.cors import CORSMiddleware
from loguru import logger


def create_app():
    _app = FastAPI(
        title=config.PROJECT_NAME,
        docs_url=f"{config.API_PREFIX}/docs",
        redoc_url=f"{config.API_PREFIX}/redoc",
        openapi_url=f"{config.API_PREFIX}/openapi.json",
        version="0.0.1",
    )

    # set cors
    if config.BACKEND_CORS_ORIGINS:
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # set routes
    @_app.get(f"{config.API_PREFIX}/healthcheck", status_code=status.HTTP_200_OK)
    def healthcheck():
        return {"status": "OK"}

    @_app.get("/", status_code=status.HTTP_200_OK)
    def root():
        return {"status": "OK"}

    logger.info(f"app created. Its ENV_NAME: {config.ENV}")
    return _app


app = create_app()
