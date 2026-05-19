from __future__ import annotations

from fastapi import FastAPI

from pyrouter.api.routes_chat import router as chat_router
from pyrouter.api.routes_models import router as models_router


def create_app() -> FastAPI:
    app = FastAPI(title="pyrouter-mvp", version="0.1.0")
    app.include_router(chat_router)
    app.include_router(models_router)
    return app


app = create_app()

