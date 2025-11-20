from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.config import Base
import uuid


class Answer(Base):
    __tablename__ = "answer"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String(255), nullable=False)
    correct = Column(Boolean, nullable=False)

    grammar_test_id = Column(UUID(as_uuid=True), nullable=False)

    grammar_test = relationship(
        "GrammarTest",
        primaryjoin="foreign(Answer.grammar_test_id) == GrammarTest.id",  # ★ 포인트
        back_populates="answers",
    )
