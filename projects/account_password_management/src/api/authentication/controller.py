from datetime import timedelta


from src.api.account.query import get_account
from src.schema.account import Account as AccountSchema

from lib.exceptions import CustomHTTPException

MAX_FAILED_VERIFICATION_ATTEMPTS = 5
BLOCK_VERIFICATION_TIME = timedelta(minutes=1)
PASSWORD_NOT_CORRECT_REASON = "Password is not correct"
TOO_MANY_FAILED_VERIFICATION_ATTEMPTS_REASON = (
    "Too many failed verification attempts, blocking one minutes"
)


class Authentication:
    def __init__(self, account: AccountSchema) -> None:
        self.__input_account: AccountSchema = account
        self.__db_account: None = None

    async def verify_account(self) -> None:
        try:
            self.__db_account = await get_account(
                username=self.__input_account.username
            )
            await self.__verify_verification_attempt()
            await self.__verify_password()
        except CustomHTTPException as exception:
            raise exception

    async def __verify_verification_attempt(self) -> None:
        return

    async def __verify_password(self) -> None:
        return
