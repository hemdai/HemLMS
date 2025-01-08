from src.schemas.common.base_schema import BaseSchema
from datetime import datetime as Datetime
from typing import Optional


class MetaSchema(BaseSchema):
    uuid: str
    path: str
    meta_type: str
    created_at: Datetime
    updated_at: Datetime
    course_id: Optional[int]
