from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags
from utils.base import SessionLocal
from src.models import ActivityModel
from src.app.activity.schemas import ActivitySchema

activity_router = APIRouter(tags=[RouteTags.ACTIVITY])
session = SessionLocal()


@activity_router.get("/activity/")
async def get_activity():
    session = SessionLocal()
    activity = session.query(ActivityModel).first()
    session.close()
    return ActivitySchema.from_orm(activity)
