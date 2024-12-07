from src.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Boolean


class Account(BaseModel):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(40))
    password = Column(String(100))
    first_name = Column(String(40))
    last_name = Column(String(40))
    disabled = Column(Boolean, default=False)
