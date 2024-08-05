from lib.exceptions import ConflictException, NotFound

USERNAME_NOT_EXISTS_REASON = "Username not exists"
USERNAME_ALREADY_EXISTS_REASON = "Username already exists"


async def create_account(account) -> None:
    try:
        return

    except:
        raise ConflictException(detail=USERNAME_ALREADY_EXISTS_REASON)


async def get_account(username: str) -> None:
    try:
        return

    except:
        raise NotFound(detail=USERNAME_NOT_EXISTS_REASON)
