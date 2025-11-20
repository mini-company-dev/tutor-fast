from uuid import UUID
from pydantic import BaseModel
from typing import List


class AnswerResponse(BaseModel):
    id: UUID
    content: str
    correct: bool

    model_config = {"from_attributes": True}


class GrammarTestResponse(BaseModel):
    id: UUID
    problem: str
    type: str
    level: str
    answers: List[AnswerResponse]

    model_config = {"from_attributes": True}
