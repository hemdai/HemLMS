from src.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from datetime import datetime
from sqlalchemy.orm import relationship


class Course(BaseModel):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    slug = Column(String, unique=True, nullable=False)
    short_description = Column(String(500))
    long_description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=True
    )
    account = relationship(
        "Account", backref="courses", lazy="joined", foreign_keys=[created_by]
    )
    categories = relationship(
        "Category",
        secondary="course_categories",
        back_populates="courses",
        lazy="joined",
    )


course_categories = Table(
    "course_categories",
    BaseModel.metadata,
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)
