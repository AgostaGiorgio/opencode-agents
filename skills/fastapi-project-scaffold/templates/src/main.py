import logging
from contextlib import asynccontextmanager
from pathlib import Path

import tomli
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.app_config import app_config
from src.di import Container
from src.routers import router

logger = logging.getLogger(__name__)

_pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
APP_VERSION = tomli.loads(_pyproject.read_text())["tool"]["poetry"]["version"]

container = Container()
container.wire(modules=[router])

app = FastAPI(title="__PROJECT_TITLE__", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins,
    allow_credentials=app_config.cors_allow_credentials,
    allow_methods=app_config.cors_allow_methods,
    allow_headers=app_config.cors_allow_headers,
)

app.include_router(router.api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=__PORT__, reload=True)
