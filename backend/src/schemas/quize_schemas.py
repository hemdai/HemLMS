from typing import Optional
from src.schemas.common.base_schema import BaseSchema


class QuizeSchema(BaseSchema):
    question: str
    answer: str
    op1: Optional[str]
    op2: Optional[str]
    op3: Optional[str]
    op4: Optional[str]
    course_id: Optional[int]
    lesson_id: Optional[int]
