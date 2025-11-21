from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from auth.auth_response import SuccessResponse

SECRET_KEY = "change_me_to_something_secure"  # 이거 나중에 바꾸자
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7일


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> SuccessResponse:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return SuccessResponse(token=token)


def verify_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
