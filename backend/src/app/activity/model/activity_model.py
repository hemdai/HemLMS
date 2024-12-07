from src.models import BaseModel, Account, Course, LessonModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import relationship
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
    lesson = relationship(
        LessonModel, backref="activities", lazy="joined", foreign_keys=[lesson_id]
    )
    course = relationship(
        Course, backref="activities", lazy="joined", foreign_keys=[course_id]
    )
    status = Column(
        SQLAlchemyEnum(StatusChoicesEnum), default=StatusChoicesEnum.STARTED
    )
    description = Column(String(1000), nullable=True)
    created_by = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=True
    )
    account = relationship(
        Account, backref="activities", lazy="joined", foreign_keys=[created_by]
    )
    created_at = Column(DateTime, default=datetime.now)
