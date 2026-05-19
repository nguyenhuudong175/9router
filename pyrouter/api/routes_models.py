from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from pyrouter.bootstrap import get_chat_service

router = APIRouter()


@router.get("/v1/models")
async def list_models():
    service = get_chat_service()
    return JSONResponse(status_code=200, content=service.list_models())

