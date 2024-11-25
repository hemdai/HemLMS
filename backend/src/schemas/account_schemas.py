from src.schemas.common.base_schema import BaseSchema
from typing import Optional


class AccountSchema(BaseSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    password: str
    disabled: Optional[bool] = False
