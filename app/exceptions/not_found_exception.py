
from app.exceptions.custom_exception import CustomException


class NotFoundException(CustomException):
    def __init__(self, message: str = "리소스를 찾을 수 없습니다."):
        super().__init__(message)
