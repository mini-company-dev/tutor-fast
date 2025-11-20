from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.config import get_session
from app.models.member import Member
from app.schemas.global_response import GlobalResponse
from app.services.member_service import MemberService
from auth.google_service import verify_google_token
from auth.jwt_utils import create_access_token
from auth.models import GoogleAuthRequest, TokenPayload

router = APIRouter(tags=["auth"])


def get_service(
    session: AsyncSession = Depends(get_session),
):
    return MemberService(session)


@router.post("/auth/google")
async def google_login(
    body: GoogleAuthRequest, service: MemberService = Depends(get_service)
):
    auth_data = await verify_google_token(body.access_token)
    if not auth_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google access token",
        )

    member: Member = await service.get_or_create(auth_data)

    payload = TokenPayload(sub=str(member.id), role=str(member.role))
    jwt_payload = payload.model_dump()

    token = create_access_token(jwt_payload)
    return GlobalResponse.success("bearer " + token)
