from fastapi import APIRouter, status
from src.api.account.query import USERNAME_NOT_EXISTS_REASON
from src.api.authentication.controller import (
    PASSWORD_NOT_CORRECT_REASON, TOO_MANY_FAILED_VERIFICATION_ATTEMPTS_REASON,
    Authentication)
from src.schema.account import Account

from lib.api_doc_response import api_doc_response
from lib.custom_response import failed_response, success_response
from lib.schema import ResponseSuccess

router = APIRouter()


@router.post(
    "/verifications",
    responses={
        status.HTTP_401_UNAUTHORIZED: api_doc_response(
            example={
                "Password is not correct": {
                    "value": failed_response(
                        reason=PASSWORD_NOT_CORRECT_REASON,
                    ),
                },
                "Too many failed verification attempts": {
                    "value": failed_response(
                        reason=TOO_MANY_FAILED_VERIFICATION_ATTEMPTS_REASON,
                    ),
                },
            }
        ),
        status.HTTP_404_NOT_FOUND: api_doc_response(
            example={
                "Username not exists": {
                    "value": failed_response(
                        reason=USERNAME_NOT_EXISTS_REASON,
                    ),
                },
            }
        ),
    },
)
async def verify_account(
    account: Account,
) -> ResponseSuccess:
    """
    - "username": a string representing the username of the account being accessed.
    - "password": a string representing the password being used to access the account. If the password verification fails five times, the user should wait one minute before attempting to verify the password again.
    """
    authentication = Authentication(account=account)
    await authentication.verify_account()

    return success_response()
