from src.models import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime


class MetaModel(BaseModel):
    __tablename__ = "meta"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(100))
    path = Column(String(100))
    meta_type = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=True
    )
