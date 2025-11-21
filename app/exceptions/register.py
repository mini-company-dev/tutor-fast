from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.exceptions.custom_exception import CustomException
from app.exceptions.exception_handler import custom_exception_handler, http_exception_handler, not_found_exception_handler, validation_exception_handler
from app.exceptions.not_found_exception import NotFoundException

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
