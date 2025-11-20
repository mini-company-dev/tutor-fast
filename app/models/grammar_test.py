from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.config import Base
import uuid


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
