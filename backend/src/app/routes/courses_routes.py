from src.schemas import CourseSchema, LessonSchema, CommentSchema, CategorySchema
from src.models import Course, LessonModel, CommentModel, Category
from utils.base import SessionLocal
from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags
from fastapi import Query

course_router = APIRouter(tags=[RouteTags.COURSE])


session = SessionLocal()


@course_router.get("/courses/")
async def get_courses(category_slug: str = Query(None)):
    if category_slug:
        courses = (
            session.query(Course)
            .filter(
                Course.categories.any(Category.slug == category_slug),
            )
            .all()
        )

        session.close()
        return [CourseSchema.from_orm(course) for course in courses]
    courses = session.query(Course).all()
    session.close()
    print([CourseSchema.from_orm(course) for course in courses])
    return [CourseSchema.from_orm(course) for course in courses]


@course_router.get("/courses/get-front-courses/")
async def get_front_courses():
    courses = session.query(Course).all()[0:3]
    session.close()
    return [CourseSchema.from_orm(course) for course in courses]


@course_router.get("/courses/{slug}")
async def get_details(slug: str):
    course_detail = session.query(Course).filter(Course.slug == slug).first()
    lessons = (
        session.query(LessonModel)
        .filter(LessonModel.course_id == course_detail.id)
        .all()
    )
    session.close()
    context = (
        {
            "course_detail": CourseSchema.from_orm(course_detail),
            "lessons": [LessonSchema.from_orm(lesson) for lesson in lessons],
        },
    )
    return context[0]


# @course_router.get("/courses/{slug}/{lesson_slug}/comments")
# async def get_lessons(slug: str, lesson_slug: str):
#     course_detail = session.query(Course).filter(Course.slug == slug).first()
#     lessons = (
#         session.query(LessonModel)
#         .filter(LessonModel.course_id == course_detail.id)
#         .all()
#     )
#     session.close()
#     return [LessonSchema.from_orm(lesson) for lesson in lessons]


@course_router.post("/courses/{slug}/{lesson_slug}/comments")
async def post_comments(slug: str, lesson_slug: str, data: dict):
    lessons = session.query(LessonModel).filter_by(slug=lesson_slug)
    course = session.query(Course).filter(Course.slug == slug).first()
    commnet = CommentModel(**data)
    commnet.lesson = lessons[0]
    commnet.course = course
    session.add(commnet)
    session.commit()
    session.refresh(commnet)
    session.close()
    return CommentSchema.from_orm(commnet)


@course_router.get("/courses/{slug}/{lesson_slug}/comments")
async def get_comments(slug: str, lesson_slug: str):
    comments = (
        session.query(CommentModel)
        .filter(
            CommentModel.lesson.has(LessonModel.slug == lesson_slug),
            CommentModel.course.has(Course.slug == slug),
        )
        .all()
    )
    session.close()
    print([CommentSchema.from_orm(comment) for comment in comments])
    return [CommentSchema.from_orm(comment) for comment in comments]


@course_router.get("/categories")
async def get_categories():
    categories = session.query(Category).all()
    session.close()
    return [CategorySchema.from_orm(category) for category in categories]
