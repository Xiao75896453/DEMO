from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from src.api import account, authentication
from lib.custom_http_exception import custom_http_exception_handler
from lib.exceptions import CustomHTTPException, UnprocessableEntityException

API_PREFIX = "api"
ACCOUNT_API_ROUTE = f"/{API_PREFIX}/accounts"
AUTHENTICATION_API_ROUTE = f"/{API_PREFIX}/authentications"

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    raise UnprocessableEntityException(detail=exc.errors())


app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)

app.include_router(
    authentication.routers.router,
    prefix=AUTHENTICATION_API_ROUTE,
    tags=["Authentication"],
)

app.include_router(
    account.routers.router,
    prefix=ACCOUNT_API_ROUTE,
    tags=["Account"],
)
