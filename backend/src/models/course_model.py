from src.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, event
from datetime import datetime
from sqlalchemy.orm import relationship
from utils.event_tools import generate_unique_slug
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum


class CourseStatusEnum(Enum):
    draft = "draft"
    published = "published"
    archived = "archived"
    in_review = "in_review"


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
    status = Column(SQLAlchemyEnum(CourseStatusEnum), default=CourseStatusEnum.draft)
    image_path = Column(String(200), nullable=True)


course_categories = Table(
    "course_categories",
    BaseModel.metadata,
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)


@event.listens_for(Course, "before_insert")
def make_slug(maper, connection, target):
    if target.title and not target.slug:
        target.slug = generate_unique_slug(
            cls=Course, target_word=target.title, connection=connection
        )
