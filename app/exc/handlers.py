from fastapi import Request
from fastapi.responses import JSONResponse

from app.exc.exception import UserNotFoundError


def not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
