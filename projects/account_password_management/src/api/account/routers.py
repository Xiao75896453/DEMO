from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.api.account.controller import (
    PASSWORD_COMPONENT_NOT_CORRECT_REASON,
    PASSWORD_TOO_LONG_REASON,
    PASSWORD_TOO_SHORT_REASON,
    USERNAME_TOO_LONG_REASON,
    USERNAME_TOO_SHORT_REASON,
    Account,
)
from src.api.account.query import USERNAME_ALREADY_EXISTS_REASON
from src.schema.account import Account as AccountSchema

from lib.api_doc_response import api_doc_response
from lib.custom_response import failed_response, success_response
from lib.schema import ResponseSuccess

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: api_doc_response(
            example={
                "Username already exists": {
                    "value": failed_response(
                        reason=USERNAME_ALREADY_EXISTS_REASON,
                    ),
                }
            }
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: api_doc_response(
            example={
                "Username is too short": {
                    "value": failed_response(
                        reason=USERNAME_TOO_SHORT_REASON,
                    ),
                },
                "Username is too long": {
                    "value": failed_response(
                        reason=USERNAME_TOO_LONG_REASON,
                    ),
                },
                "Password is too short": {
                    "value": failed_response(
                        reason=PASSWORD_TOO_SHORT_REASON,
                    ),
                },
                "Password is too long": {
                    "value": failed_response(
                        reason=PASSWORD_TOO_LONG_REASON,
                    ),
                },
                "Password component is not correct": {
                    "value": failed_response(
                        reason=PASSWORD_COMPONENT_NOT_CORRECT_REASON,
                    ),
                },
            },
        ),
    },
)
async def create_account(
    account_data: AccountSchema,
) -> ResponseSuccess:
    """
    - "username": a string representing the desired username for the account, with a minimum length of 3 characters and a maximum length of 32 characters.
    - "password": a string representing the desired password for the account, with a minimum length of 8 characters and a maximum length of 32 characters, containing at least 1 uppercase letter, 1 lowercase letter, and 1 number.
    """
    account = Account(account_data)
    await account.create_account()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=success_response())
