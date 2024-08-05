from pydantic import BaseModel


class ResponseSuccess(BaseModel):
    success: bool = True
    reason: None = None
