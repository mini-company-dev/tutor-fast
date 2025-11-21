from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exceptions.custom_exception import CustomException
from app.exceptions.not_found_exception import NotFoundException
from app.schemas.global_response import GlobalResponse


def print_error(request: Request, exc: Exception, status: int):
    print("====== ERROR ======")
    print(f"URL: {request.method} {request.url}")
    print(f"ErrorType: {exc.__class__.__name__}")
    print(f"Message: {str(exc)}")
    print(f"Status: {status}")
    print("====================")


# 400 Bad Request
async def custom_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, CustomException)

    http_status = 400
    print_error(request, exc, http_status)

    return JSONResponse(
        status_code=http_status,
        content=GlobalResponse.error(exc.message).model_dump(),
    )


# 404 Not Found
async def not_found_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, NotFoundException)

    http_status = 404
    print_error(request, exc, http_status)

    return JSONResponse(
        status_code=http_status,
        content=GlobalResponse.error(exc.message).model_dump(),
    )


# HTTPException: FastAPI 기본 status 유지
async def http_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, HTTPException)

    http_status = exc.status_code
    print_error(request, exc, http_status)

    return JSONResponse(
        status_code=http_status,
        content=GlobalResponse.error(exc.detail).model_dump(),
    )


# 422 Validation Error
async def validation_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, RequestValidationError)

    http_status = 422
    print_error(request, exc, http_status)

    return JSONResponse(
        status_code=http_status,
        content=GlobalResponse.error("Validation Error").model_dump(),
    )
