from src.schemas import (
    CourseSchema,
    LessonSchema,
    CommentSchema,
    CategorySchema,
    AccountSchema,
    CreateCourseSchema,
)
from src.models import (
    Course,
    LessonModel,
    CommentModel,
    Category,
    Account,
    CourseStatusEnum,
)
from utils.base import SessionLocal
from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags
from fastapi import Query, Depends, UploadFile
from src.app.routes.account_routes import get_current_user
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from utils.db_tools import add_model_records
from utils.base import save_file

course_router = APIRouter(tags=[RouteTags.COURSE])


@course_router.get("/courses/")
async def get_courses(category_slug: str = Query(None)):
    session = SessionLocal()
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
    return [CourseSchema.from_orm(course) for course in courses]


@course_router.get("/courses/get-front-courses/")
async def get_front_courses():
    session = SessionLocal()
    courses = session.query(Course).filter(Course.status == CourseStatusEnum.draft)[0:3]
    session.close()
    return [CourseSchema.from_orm(course) for course in courses]


@course_router.get("/courses/{slug}")
async def get_details(slug: str):
    session = SessionLocal()
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
    session = SessionLocal()
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
    session = SessionLocal()
    comments = (
        session.query(CommentModel)
        .filter(
            CommentModel.lesson.has(LessonModel.slug == lesson_slug),
            CommentModel.course.has(Course.slug == slug),
        )
        .all()
    )
    session.close()
    return [CommentSchema.from_orm(comment) for comment in comments]


@course_router.get("/categories")
async def get_categories():
    session = SessionLocal()
    categories = session.query(Category).all()
    session.close()
    return [CategorySchema.from_orm(category) for category in categories]


@course_router.get("/authors/courses/{account_id}")
async def get_authors_courses_for_user(account_id: int):
    """Get all courses created by selected author from user view"""
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == account_id).first()
    courses = (
        session.query(Course).filter(Course.account.has(Account.id == account.id)).all()
    )
    session.close()
    courses_data = [CourseSchema.from_orm(course) for course in courses]
    account_data = AccountSchema.from_orm(account)
    return {"account": account_data, "courses_data": courses_data}


@course_router.get("/authors/courses")
async def get_authors_all_courses_for_author(
    account: Account = Depends(get_current_user),
):
    """Get all courses created by selected author from user view"""
    session = SessionLocal()
    courses = (
        session.query(Course).filter(Course.account.has(Account.id == account.id)).all()
    )
    session.close()
    courses_data = [CourseSchema.from_orm(course) for course in courses]
    return courses_data


@course_router.post("/create/courses")
async def create_courses(
    data: CreateCourseSchema, account: Account = Depends(get_current_user)
):
    session = SessionLocal()
    account = session.merge(account)
    categories = session.query(Category).filter(Category.id.in_(data.categories)).all()
    if not categories or len(categories) != len(data.categories):
        session.close()
        raise HTTPException(status_code=400, detail="Invalid categories")

    course = Course(
        title=data.title,
        short_description=data.short_description,
        long_description=data.long_description,
        categories=categories,
        created_by=account.id,
        status=data.status,
    )
    course_model, session = add_model_records(
        Course, course, session=session, sesson_close=False
    )
    lesson_list = []
    if data.lessons:
        for lesson in data.lessons:
            lesson_instance = LessonModel(
                title=lesson.title,
                short_description=lesson.short_description,
                long_description=lesson.long_description,
                video_url=lesson.video_url,
                course_id=course.id,
            )
            lesson_list.append(lesson_instance)
        lesson_list_model, session = add_model_records(
            LessonModel, lesson_list, session=session, sesson_close=False
        )

    session.refresh(course_model)
    session.close()

    return CourseSchema.from_orm(course)


@course_router.post("/create-course-with-lessons")
async def create_course_with_lessons(
    data: CreateCourseSchema, account: Account = Depends(get_current_user)
):
    session = SessionLocal()
    account = session.merge(account)
    categories = session.query(Category).filter(Category.id.in_(data.categories)).all()
    if not categories or len(categories) != len(data.categories):
        session.close()
        raise HTTPException(status_code=400, detail="Invalid categories")

    course = Course(
        title=data.title,
        short_description=data.short_description,
        long_description=data.long_description,
        categories=categories,
        account=account,
        status=data.status,
    )
    course.categories = categories
    try:
        session.add(course)
        session.commit()
        session.refresh(course)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    lesson_list = []
    for lesson in data.lessons:
        lesson = LessonModel(
            title=lesson.title,
            short_description=lesson.short_description,
            long_description=lesson.long_description,
            video_url=lesson.video_url,
            course_id=course.id,
        )
        lesson_list.append(lesson)
    try:
        session.add_all(lesson_list)
        session.commit()
        session.refresh(course)
        session.close()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return CourseSchema.from_orm(course)


@course_router.post("/course/images/{slug}")
async def upload_course_images(slug: str, file: UploadFile):
    saving_path = save_file(file=file, document_type="image")
    if not saving_path:
        raise HTTPException(status_code=400, detail="Failed to save file")
    session = SessionLocal()
    course = session.query(Course).filter(Course.slug == slug).first()
    course.image_path = saving_path
    session.commit()
    session.close()
    return {"url": saving_path, "message": "File uploaded successfully"}
