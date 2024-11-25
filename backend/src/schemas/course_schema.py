from typing import Optional, List, Any
from datetime import datetime
from src.schemas.common import BaseSchema
from src.schemas.category_schema import CategorySchema


class CourseSchema(BaseSchema):
    title: str
    slug: Optional[str]
    short_description: Optional[str]
    long_description: Optional[str]
    categories: Optional[List[CategorySchema]]
    created_at: Optional[datetime]
