from pydantic import BaseModel


class AuthResponse(BaseModel):
    provider: str
    username: str
    email: str
    name: str
    picture: str

class SuccessResponse(BaseModel):
    token: str