from pydantic import BaseModel

class HistoryRequest(BaseModel):
    user: str
    assistant: str

class TutorResponse(BaseModel):
    user: str
    reply: str
    pronunciation: int
    fluency: int
    coherence: int
