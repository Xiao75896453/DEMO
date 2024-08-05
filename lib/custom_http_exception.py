from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from lib.custom_response import failed_response


def custom_http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content=failed_response(exc.detail),
        headers=exc.headers,
    )
