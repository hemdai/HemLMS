from src.schemas import QuizeSchema
from src.models import QuizModel, LessonModel, Course
from utils.base import SessionLocal
from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags

quize_router = APIRouter(tags=[RouteTags.COURSE])


@quize_router.get("/quizes/{course_slug}/{lesson_slug}")
async def get_quizes(course_slug: str = None, lesson_slug: str = None):
    if lesson_slug and course_slug:
        session = SessionLocal()
        quizes = (
            session.query(QuizModel)
            .join(Course, QuizModel.course_id == Course.id)
            .join(LessonModel, QuizModel.lesson_id == LessonModel.id)
            .filter(LessonModel.slug == lesson_slug, Course.slug == course_slug)
            .all()
        )
        session.close()
        return [QuizeSchema.from_orm(quize) for quize in quizes]


@quize_router.get("/quizes/{quize_id}")
async def get_quize(quize_id: int):
    session = SessionLocal()
    quize = session.query(QuizModel).filter(QuizModel.id == quize_id).first()
    session.close()
    return QuizeSchema.from_orm(quize)


@quize_router.post("/quizes/")
async def post_quize(data: dict):
    session = SessionLocal()
    quize = QuizModel(**data)
    session.add(quize)
    session.commit()
    session.refresh(quize)
    session.close()
    return QuizeSchema.from_orm(quize)


@quize_router.put("/quizes/{quize_id}")
async def update_quize(quize_id: int, data: dict):
    session = SessionLocal()
    quize = session.query(QuizModel).filter(QuizModel.id == quize_id).first()
    for key, value in data.items():
        setattr(quize, key, value)
    session.commit()
    session.refresh(quize)
    session.close()
    return QuizeSchema.from_orm(quize)


@quize_router.delete("/quizes/{quize_id}")
async def delete_quize(quize_id: int):
    session = SessionLocal()
    quize = session.query(QuizModel).filter(QuizModel.id == quize_id).first()
    session.delete(quize)
    session.commit()
    session.close()
    return QuizeSchema.from_orm(quize)
