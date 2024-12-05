from src.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from datetime import datetime


class QuizModel(BaseModel):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(1000))
    answer = Column(String(1000))
    op1 = Column(String(1000))
    op2 = Column(String(1000))
    op3 = Column(String(1000))
    op4 = Column(String(1000))
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=True
    )
    lesson_id = Column(
        Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True
    )
