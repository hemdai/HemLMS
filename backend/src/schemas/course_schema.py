from typing import Optional, List, Any
from datetime import datetime
from src.schemas.common import BaseSchema
from src.schemas.account_schemas import AccountSchema
from src.schemas.category_schema import CategorySchema


class CourseSchema(BaseSchema):
    title: str
    slug: Optional[str]
    short_description: Optional[str]
    long_description: Optional[str]
    categories: Optional[List[CategorySchema]]
    created_at: Optional[datetime]
    course_image: str = "127.0.0.1:5000/"
    account: Optional[AccountSchema]
    created_by: Optional[int]
