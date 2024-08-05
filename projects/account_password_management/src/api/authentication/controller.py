from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from src.api.account.query import get_account, update_account
from src.models.account import Account as AccountModel
from src.schema.account import Account as AccountSchema
from src.utils.password import pwd_context

from lib.exceptions import CustomHTTPException, Unauthorized

MAX_FAILED_VERIFICATION_ATTEMPTS = 5
BLOCK_VERIFICATION_TIME = timedelta(minutes=1)
PASSWORD_NOT_CORRECT_REASON = "Password is not correct"
TOO_MANY_FAILED_VERIFICATION_ATTEMPTS_REASON = (
    "Too many failed verification attempts, blocking one minutes"
)


class Authentication:
    def __init__(self, account: AccountSchema) -> None:
        self.__input_account: AccountSchema = account
        self.__db_account: AccountModel | None = None

    async def verify_account(self, db_session: Session) -> None:
        try:
            self.__db_account = await get_account(
                username=self.__input_account.username, db_session=db_session
            )
            await self.__verify_verification_attempt(db_session=db_session)
            await self.__verify_password(db_session=db_session)
        except CustomHTTPException as exception:
            raise exception

    async def __verify_verification_attempt(self, db_session: Session) -> None:
        if self.__db_account.failed_attempts >= MAX_FAILED_VERIFICATION_ATTEMPTS:
            if self.__db_account.block_verification_time > datetime.now():
                raise Unauthorized(detail=TOO_MANY_FAILED_VERIFICATION_ATTEMPTS_REASON)
            else:
                await self.__reset_account_failed_attempt(db_session=db_session)

    async def __verify_password(self, db_session: Session) -> None:
        if not pwd_context.verify(
            self.__input_account.password, self.__db_account.password
        ):
            await self.__accumulate_account_failed_attempt(db_session=db_session)

            raise Unauthorized(detail=PASSWORD_NOT_CORRECT_REASON)
        else:
            await self.__reset_account_failed_attempt(db_session=db_session)

    async def __accumulate_account_failed_attempt(self, db_session: Session) -> None:
        if self.__db_account.failed_attempts >= MAX_FAILED_VERIFICATION_ATTEMPTS - 1:
            block_verification_time = datetime.now() + BLOCK_VERIFICATION_TIME
        else:
            block_verification_time = None

        await update_account(
            username=self.__db_account.username,
            account={
                "failed_attempts": self.__db_account.failed_attempts + 1,
                "block_verification_time": block_verification_time,
            },
            db_session=db_session,
        )

    async def __reset_account_failed_attempt(self, db_session: Session) -> None:
        await update_account(
            username=self.__db_account.username,
            account={
                "failed_attempts": 0,
                "block_verification_time": None,
            },
            db_session=db_session,
        )
