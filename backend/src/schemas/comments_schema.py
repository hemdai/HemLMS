from src.schemas.common.base_schema import BaseSchema
from src.schemas import AccountSchema, CourseSchema, LessonSchema
from typing import Optional
from datetime import datetime


class CommentSchema(BaseSchema):
    name: str
    content: str
    created_at: Optional[datetime]
    account_id: Optional[int]
    course_id: Optional[int]
    lesson_id: Optional[int]
    course: Optional[CourseSchema]
    lesson: Optional[LessonSchema]
    account: Optional[AccountSchema]
