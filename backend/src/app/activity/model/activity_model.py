from src.models import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum


class StatusChoicesEnum(Enum):
    STARTED = "started"
    DONE = "done"


class ActivityModel(BaseModel):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=True
    )
    lesson_id = Column(
        Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True
    )
    status = Column(
        SQLAlchemyEnum(StatusChoicesEnum), default=StatusChoicesEnum.STARTED
    )
    description = Column(String(1000), nullable=True)
    created_by = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.now)
