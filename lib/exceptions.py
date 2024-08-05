from fastapi import HTTPException, status


class AppException(Exception):
    pass


class CustomHTTPException(AppException, HTTPException):
    pass


class UnprocessableEntityException(CustomHTTPException):
    def __init__(self, detail: str | dict) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class ConflictException(CustomHTTPException):
    def __init__(self, detail: str | dict) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class Unauthorized(CustomHTTPException):
    def __init__(self, detail: str | dict) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class NotFound(CustomHTTPException):
    def __init__(self, detail: str | dict) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
