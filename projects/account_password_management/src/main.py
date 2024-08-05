from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from lib.custom_http_exception import custom_http_exception_handler
from lib.exceptions import CustomHTTPException, UnprocessableEntityException

API_PREFIX = "api"

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    raise UnprocessableEntityException(detail=exc.errors())


app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
