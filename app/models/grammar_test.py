from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.config import Base
import uuid


from enum import Enum


class LEVEL(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"


class TEST_TYPE(str, Enum):
    GRAMMAR = "Grammar"
    VOCABULARY = "Vocabulary"


class GrammarTest(Base):
    __tablename__ = "grammar_test"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    level = Column(String(255), nullable=False)

    answers = relationship(
        "Answer",
        primaryjoin="GrammarTest.id == foreign(Answer.grammar_test_id)",
        back_populates="grammar_test",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


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
