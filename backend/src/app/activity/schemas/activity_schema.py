from src.schemas.common.base_schema import BaseSchema
from typing import Optional, Union
from datetime import datetime
from src.app.activity.model.activity_model import StatusChoicesEnum
from pydantic import validator


class ActivitySchema(BaseSchema):
    course_id: Optional[int]
    lesson_id: Optional[int]
    status: Optional[StatusChoicesEnum]
    description: Optional[str]
    created_by: Optional[int]
    created_at: Optional[Union[datetime, str]] = None

    @validator("created_at", pre=True, always=True)
    def parse_created_at(cls, value):
        if value == "":
            return None
