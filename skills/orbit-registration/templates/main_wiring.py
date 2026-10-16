"""main.py wiring fragment for Orbit registration.

Merge these pieces into the project's existing main.py. Do not replace CORS,
container wiring, or routers.

Key points:
- APP_VERSION is read from pyproject [tool.poetry].version (needs tomli).
- orbit_client exists only when orbit_api_url is set; keep the guard identical
  in lifespan.
- BOTH lifespan branches must yield.
"""

import logging
from pathlib import Path
from contextlib import asynccontextmanager

import tomli
from fastapi import FastAPI

from src.config.app_config import app_config
from src.clients.orbit_client import OrbitClient

logger = logging.getLogger(__name__)

_pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
APP_VERSION = tomli.loads(_pyproject.read_text())["tool"]["poetry"]["version"]

if app_config.orbit_api_url:
    orbit_client = OrbitClient(
        orbit_api_url=app_config.orbit_api_url,
        name="<ServiceName>",                 # stable, human-readable service name
        version=APP_VERSION,
        description="<short description>",    # one-line description of the service
        app_url=app_config.app_url,           # MUST be a full http(s) URL
        # icon="https://.../icon.png",        # optional; must be a URL if set
        # ping_interval_seconds=3600,         # default: 1h
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    if app_config.orbit_api_url:
        orbit_client.start()
        yield
        orbit_client.stop()
    else:
        yield  # ALWAYS yield: without this the app fails to start when Orbit is off


app = FastAPI(lifespan=lifespan, title="<ServiceName> API", version=APP_VERSION)

# ... keep the project's existing CORS / Container().wire(...) / include_router ...
