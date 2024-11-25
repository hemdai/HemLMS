from src.models import Category, Course

from utils.base import SessionLocal

session = SessionLocal()

category = session.query(Category).filter(Category.id == 1).first()

course = session.query(Course).filter(Course.id == 1).first()

category.courses.append(course)

session.commit()
