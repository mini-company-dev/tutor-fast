from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi import Depends
from typing import List, Optional
import json

from app.schemas.ai_test_response import HistoryRequest, TutorResponse
from app.schemas.global_response import GlobalResponse
from app.services.ai_test_service import AiTestService

router = APIRouter(prefix="/api/aiTest", tags=["AiTest"])


def get_service():
    return AiTestService()


@router.post("", response_model=GlobalResponse[TutorResponse])
async def evaluate(
    file: UploadFile = File(...),
    history: Optional[str] = Form(None),
    service: AiTestService = Depends(get_service),
):
    # 파일 체크
    if file is None:
        raise HTTPException(status_code=400, detail="음성 파일이 필요합니다.")

    # history 파싱
    try:
        history_raw = json.loads(history) if history else []
        history_list: List[HistoryRequest] = [
            HistoryRequest(**item) for item in history_raw
        ]
    except Exception:
        raise HTTPException(status_code=400, detail="history 파싱 실패")

    data = await service.evaluate(file, history_list)
    return GlobalResponse.success(data)
