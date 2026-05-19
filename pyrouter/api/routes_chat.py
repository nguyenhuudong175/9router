from __future__ import annotations

from fastapi import APIRouter, Header, Request
from fastapi.responses import JSONResponse

from pyrouter.bootstrap import get_chat_service

router = APIRouter()


@router.post("/v1/chat/completions")
async def chat_completions(
    request: Request,
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None),
):
    body = await request.json()
    service = get_chat_service()
    result = service.handle_chat(
        body,
        headers={"authorization": authorization or "", "x-api-key": x_api_key or ""},
    )
    return JSONResponse(status_code=result.status, content=result.body)


@router.post("/v1/messages")
async def claude_messages(request: Request, authorization: str | None = Header(default=None), x_api_key: str | None = Header(default=None)):
    body = await request.json()
    service = get_chat_service()
    result = service.handle_chat(body, headers={"authorization": authorization or "", "x-api-key": x_api_key or ""})
    return JSONResponse(status_code=result.status, content=result.body)


@router.post("/v1/responses")
async def openai_responses(request: Request, authorization: str | None = Header(default=None), x_api_key: str | None = Header(default=None)):
    body = await request.json()
    service = get_chat_service()
    result = service.handle_chat(body, headers={"authorization": authorization or "", "x-api-key": x_api_key or ""})
    return JSONResponse(status_code=result.status, content=result.body)

