from src.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from src.models import Account, Course, LessonModel


class CommentModel(BaseModel):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    content = Column(String((500)))
    created_at = Column(DateTime, default=datetime.now)
    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=True
    )
    account = relationship(
        Account, backref="comments", lazy="joined", foreign_keys=[account_id]
    )
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=True
    )
    course = relationship(
        Course, backref="comments", lazy="joined", foreign_keys=[course_id]
    )
    lesson_id = Column(
        Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True
    )
    lesson = relationship(
        LessonModel, backref="comments", lazy="joined", foreign_keys=[lesson_id]
    )
