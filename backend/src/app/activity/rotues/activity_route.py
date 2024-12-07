from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags
from utils.base import SessionLocal
from src.models import ActivityModel, Account
from src.app.activity.schemas import ActivitySchema


activity_router = APIRouter(tags=[RouteTags.ACTIVITY])
session = SessionLocal()


@activity_router.get("/activity/")
async def get_activity():
    session = SessionLocal()
    activity = (
        session.query(Account).filter(Account.activities.status == "started").first()
    )
    session.close()
    return ActivitySchema.from_orm(activity)


@activity_router.get("/active/coureses")
async def active_courses(data: dict):
    session = SessionLocal()
    activity = (
        session.query(Account).filter(Account.activities.status == "started").first()
    )
    session.close()
    return {"records": ActivitySchema.from_orm(activity)}
