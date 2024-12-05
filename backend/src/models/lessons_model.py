from src.models.base_model import BaseModel
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from datetime import datetime
from sqlalchemy import event
from utils.event_tools import generate_unique_slug


class LessonStatusEnum(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class LessonTypeEnum(Enum):
    VIDEO = "video"
    ARTICLE = "article"
    QUIZ = "quiz"


class LessonModel(BaseModel):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=True
    )
    lesson_type = Column(SQLAlchemyEnum(LessonTypeEnum), default=LessonTypeEnum.VIDEO)
    short_description = Column(String(500))
    long_description = Column(String(1000))
    status = Column(SQLAlchemyEnum(LessonStatusEnum), default=LessonStatusEnum.DRAFT)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    slug = Column(String, unique=True, nullable=True)
    video_url = Column(String(100), nullable=True)

    def __str__(self):
        return self.title


@event.listens_for(LessonModel, "before_insert")
def make_slug(maper, connection, target):
    if target.title and not target.slug:
        target.slug = generate_unique_slug(
            cls=LessonModel, target_word=target.title, connection=connection
        )
