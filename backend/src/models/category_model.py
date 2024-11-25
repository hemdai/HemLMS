from src.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship


class Category(BaseModel):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    slug = Column(String, unique=True, nullable=False)
    short_description = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    courses = relationship(
        "Course",
        secondary="course_categories",
        back_populates="categories",
        lazy="joined",
    )
