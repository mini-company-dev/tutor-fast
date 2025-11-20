from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import random

from app.models.grammar_test import GrammarTest
from app.schemas.grammar_test import GrammarTestResponse


class GrammarTestService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self):
        stmt = select(GrammarTest).options(selectinload(GrammarTest.answers))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_one(self, id: str):
        stmt = (
            select(GrammarTest)
            .where(GrammarTest.id == id)
            .options(selectinload(GrammarTest.answers))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_level(self, level: str, type: str):
        stmt = (
            select(GrammarTest)
            .where(
                GrammarTest.level == level,
                GrammarTest.type == type,
            )
            .options(selectinload(GrammarTest.answers))
        )

        result = await self.session.execute(stmt)
        tests = list(result.scalars().all())
        random.shuffle(tests)
        return [GrammarTestResponse.model_validate(item) for item in tests]
