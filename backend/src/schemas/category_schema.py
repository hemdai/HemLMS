from typing import Optional, List, Any
from datetime import datetime
from src.schemas.common.base_schema import BaseSchema


class CategorySchema(BaseSchema):
    title: str
    slug: Optional[str]
    short_description: Optional[str]
    created_at: Optional[datetime]
