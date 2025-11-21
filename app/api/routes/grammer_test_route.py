from fastapi import APIRouter, Depends, Query
from typing import List

from app.enums.level import LEVEL
from app.enums.test_type import TEST_TYPE
from app.schemas.global_response import GlobalResponse
from app.schemas.grammar_test_response import GrammarTestResponse
from app.services.grammar_test_service import GrammarTestService

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.config import get_session
from auth.deps import get_current_user

router = APIRouter(prefix="/api/tests", tags=["GrammarTest"])


def get_service(
    session: AsyncSession = Depends(get_session),
):
    return GrammarTestService(session)


@router.get("/{id}", response_model=GlobalResponse[GrammarTestResponse])
async def get_test(
    id: str,
    service: GrammarTestService = Depends(get_service),
    user=Depends(get_current_user),
):
    data = await service.find_one(id)
    return GlobalResponse.success(data)


@router.get("/", response_model=GlobalResponse[List[GrammarTestResponse]])
async def get_tests_by_level(
    level: LEVEL = Query(...),
    type: TEST_TYPE = Query(...),
    service: GrammarTestService = Depends(get_service),
    user=Depends(get_current_user),
):
    data = await service.get_by_level(level, type)
    return GlobalResponse.success(data)
