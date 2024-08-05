import re

from sqlalchemy.orm import Session
from src.api import account
from src.schema.account import Account as AccountSchema

from lib.exceptions import CustomHTTPException, UnprocessableEntityException

MIN_USERNAME_LEN = 3
MAX_USERNAME_LEN = 32
MIN_PASSWORD_LEN = 8
MAX_PASSWORD_LEN = 32
USERNAME_TOO_SHORT_REASON = "Username is too short"
USERNAME_TOO_LONG_REASON = "Username is too long"
PASSWORD_TOO_SHORT_REASON = "Password is too short"
PASSWORD_TOO_LONG_REASON = "Password is too long"
PASSWORD_COMPONENT_NOT_CORRECT_REASON = (
    "Password not contain at least 1 uppercase letter, 1 lowercase letter, and 1 number"
)
AT_LEAST_ONE_UPPERCASE_LETTER_ONE_LOWERCASE_LETTER_ONE_NUMBER_REGEX = (
    r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$"
)


class Account:
    def __init__(self, account: AccountSchema) -> None:
        self.__account: AccountSchema = account

    async def create_account(self) -> None:
        try:
            await self.__verify_created_account_format()
            await self.__hash_password()
            await account.query.create_account(self.__account)

        except CustomHTTPException as exception:
            raise exception

    async def __verify_created_account_format(self) -> None:
        try:
            await self.__verify_username_format()
            await self.__verify_password_format()

        except UnprocessableEntityException as exception:
            raise exception

    async def __verify_username_format(self) -> None:
        try:
            await self.__verify_username_len(len(self.__account.username))

        except UnprocessableEntityException as exception:
            raise exception

    async def __verify_username_len(self, username_len: int) -> None:
        if username_len < MIN_USERNAME_LEN:
            raise UnprocessableEntityException(detail=USERNAME_TOO_SHORT_REASON)

        elif username_len > MAX_USERNAME_LEN:
            raise UnprocessableEntityException(detail=USERNAME_TOO_LONG_REASON)

    async def __verify_password_format(self) -> None:
        try:
            await self.__verify_password_len(len(self.__account.password))
            await self.__verify_password_component(self.__account.password)

        except UnprocessableEntityException as exception:
            raise exception

    async def __verify_password_len(self, password_len: int) -> None:
        if password_len < MIN_PASSWORD_LEN:
            raise UnprocessableEntityException(detail=PASSWORD_TOO_SHORT_REASON)

        elif password_len > MAX_PASSWORD_LEN:
            raise UnprocessableEntityException(detail=PASSWORD_TOO_LONG_REASON)

    async def __verify_password_component(self, password: str) -> None:
        password_pattern = re.compile(
            AT_LEAST_ONE_UPPERCASE_LETTER_ONE_LOWERCASE_LETTER_ONE_NUMBER_REGEX
        )

        if not password_pattern.match(password):
            raise UnprocessableEntityException(
                detail=PASSWORD_COMPONENT_NOT_CORRECT_REASON
            )

    async def __hash_password(self) -> None:
        return
