from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags
from utils.base import SessionLocal, add_model_records
from src.models import ActivityModel, Account, Course, LessonModel
from src.schemas import CourseSchema
from src.app.activity.schemas import ActivitySchema
from src.app.activity.model.activity_model import StatusChoicesEnum
from sqlalchemy import select
from fastapi import Depends
from src.app.routes.account_routes import get_current_user
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

activity_router = APIRouter(tags=[RouteTags.ACTIVITY])
session = SessionLocal()


@activity_router.get("/activity")
async def get_activity():
    session = SessionLocal()
    activities = session.query(ActivityModel).all()
    session.close()
    return [ActivitySchema.from_orm(activity) for activity in activities]


@activity_router.get("/active/get-active-courses")
async def active_courses(account: Account = Depends(get_current_user)):
    session = SessionLocal()
    try:
        account = session.merge(account)
        courses = []
        for activity in account.activities:
            if (
                activity.status == StatusChoicesEnum.STARTED
                and activity.course not in courses
            ):
                courses.append(activity.course)
        return {"records": [CourseSchema.from_orm(course) for course in courses]}
    finally:
        session.close()

    # records = (
    #     session.execute(
    #         select(ActivityModel)
    #         .where(ActivityModel.status == StatusChoicesEnum.STARTED)
    #         .where(ActivityModel.created_by == account.id)
    #     )
    #     .unique()
    #     .scalars()
    #     .all()
    # )

    # return {"records": [CourseSchema.from_orm(course) for course in courses]}


@activity_router.post("/activity/track-started/{course_slug}/{lesson_slug}")
async def track_start_activity(
    account: Account = Depends(get_current_user),
    course_slug: str = None,
    lesson_slug: str = None,
):
    session = SessionLocal()
    course = session.query(Course).filter(Course.slug == course_slug).first()
    lesson = session.query(LessonModel).filter(LessonModel.slug == lesson_slug).first()
    account = session.merge(account)

    activity_record = (
        session.query(ActivityModel)
        .filter(
            ActivityModel.course == course,
            ActivityModel.lesson == lesson,
            ActivityModel.created_by == account.id,
        )
        .first()
    )

    if activity_record is None:
        activity_record = ActivityModel(
            course=course,
            lesson=lesson,
            created_by=account.id,
            status=StatusChoicesEnum.STARTED,
        )
        try:
            session.add(activity_record)
            session.commit()
            session.refresh(activity_record)
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            session.close()
    return ActivitySchema.from_orm(activity_record)


@activity_router.post("/activity/track-completed/{course_slug}/{lesson_slug}")
async def track_completed_activity(
    account: Account = Depends(get_current_user),
    course_slug: str = None,
    lesson_slug: str = None,
):
    session = SessionLocal()
    account = session.merge(account)
    course_activity = (
        session.query(ActivityModel)
        .filter(
            ActivityModel.course.has(Course.slug == course_slug),
            ActivityModel.lesson.has(LessonModel.slug == lesson_slug),
            ActivityModel.created_by == account.id,
        )
        .first()
    )
    if course_activity:
        course_activity.status = StatusChoicesEnum.DONE
        session.commit()
        session.refresh(course_activity)
        session.close()
        return ActivitySchema.from_orm(course_activity)
