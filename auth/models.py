from pydantic import BaseModel


class GoogleAuthRequest(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: str
    role: str
