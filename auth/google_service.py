from tkinter import NO
import httpx

from auth.auth_response import AuthResponse

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

async def verify_google_token(access_token: str) -> AuthResponse | None:
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_USERINFO_URL, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    return AuthResponse(
        provider="google",
        username=data.get("id"),
        email=data.get("email"),
        name=data.get("name"),
        picture=data.get("picture"),
    )
