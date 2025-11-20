from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class GlobalResponse(BaseModel, Generic[T]):
    message: Optional[str] = None
    code: int = 0
    data: Optional[T] = None

    @staticmethod
    def success(data: T) -> "GlobalResponse[T]":
        return GlobalResponse[T](message=None, code=0, data=data)

    @staticmethod
    def ok() -> "GlobalResponse[None]":
        return GlobalResponse[None](message=None, code=0, data=None)

    @staticmethod
    def error(message: str, code: int) -> "GlobalResponse[None]":
        return GlobalResponse[None](message=message, code=code, data=None)
