from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.member import Member
from auth.auth_response import AuthResponse


class MemberService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, auth_data: AuthResponse) -> Member:
        data = await self.get_by_username(auth_data.username)
        if data:
            return data
        return await self.create_member(auth_data)

    async def get_by_username(self, username: str) -> Member | None:
        stmt = select(Member).where(
            Member.username == username,
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_member(self, auth_data: AuthResponse) -> Member:
        user = Member(
            provider=auth_data.provider,
            username=auth_data.username,
            email=auth_data.email,
            name=auth_data.name,
            picture=auth_data.picture,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
