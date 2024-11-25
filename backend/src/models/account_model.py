from src.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Boolean


class Account(BaseModel):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20))
    password = Column(String(100))
    first_name = Column(String(20))
    last_name = Column(String(20))
    disabled = Column(Boolean, default=False)
