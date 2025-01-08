from typing import Optional, List, Any
from datetime import datetime
from src.schemas.common import BaseSchema
from src.schemas.account_schemas import AccountSchema
from src.schemas.category_schema import CategorySchema
from src.models import CourseStatusEnum
from src.schemas.lesson_schema import CreateLessonSchema


class CourseSchema(BaseSchema):
    title: str
    slug: Optional[str]
    short_description: Optional[str]
    long_description: Optional[str]
    status: Optional[CourseStatusEnum]
    created_at: Optional[datetime]
    image_path: Optional[str]
    created_by: Optional[int]
    account: Optional[AccountSchema]
    categories: Optional[List[CategorySchema]]


class CreateCourseSchema(BaseSchema):
    title: str
    short_description: Optional[str]
    long_description: Optional[str]
    categories: Optional[List[int]]
    status: Optional[CourseStatusEnum]
    lessons: Optional[List[CreateLessonSchema]]
    image_path: Optional[str]
    image_uuid: Optional[str]
