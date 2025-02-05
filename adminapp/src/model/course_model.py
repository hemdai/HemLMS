from src.model.base_model import BaseModel
from sqlalchemy import Integer, Column, String


class CourseModel(BaseModel):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(100))
    slug = Column(String, unique=True, nullable=False)
    short_description = Column(String(500))
    long_description = Column(String(1000))
