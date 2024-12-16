from typing import Optional, List, Any
from datetime import datetime
from src.schemas.common.base_schema import BaseSchema


class LessonSchema(BaseSchema):
    title: str
    slug: Optional[str]
    short_description: Optional[str]
    long_description: Optional[str]
    course_id: Optional[int]
    lesson_type: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    video_url: Optional[str]


class CreateLessonSchema(BaseSchema):
    title: str
    short_description: Optional[str]
    long_description: Optional[str]
    video_url: Optional[str]
