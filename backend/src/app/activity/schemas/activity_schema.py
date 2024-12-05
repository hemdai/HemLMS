from src.schemas.common.base_schema import BaseSchema
from typing import Optional
from datetime import datetime
from src.app.activity.model.activity_model import StatusChoicesEnum


class ActivitySchema(BaseSchema):
    course_id: Optional[int]
    lesson_id: Optional[int]
    status: Optional[StatusChoicesEnum]
    description: Optional[str]
    created_by: Optional[int]
    created_at: Optional[datetime]
