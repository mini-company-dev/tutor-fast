import uuid
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.config import Base
from app.enums.member_role import MEMBER_ROLE
from app.enums.member_status import MEMBER_STATUS


class Member(Base):
    __tablename__ = "member"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    provider = Column(String(255), nullable=True)
    username = Column(String(255), unique=True, nullable=False)

    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    picture = Column(
        String(255),
        nullable=False,
        default="https://tutor-s3.s3.ap-northeast-2.amazonaws.com/profile.jpg",
    )

    role = Column(String(255), nullable=False, default=MEMBER_ROLE.USER.value)
    status = Column(String(255), nullable=False, default=MEMBER_STATUS.ACTIVE.value)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
