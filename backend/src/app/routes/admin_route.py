# /admin/tables
from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags
from utils.base import SessionLocal
from src.models import __all__, LessonTypeEnum, LessonStatusEnum
import importlib

admin_router = APIRouter(tags=[RouteTags.ACCOUNT])


@admin_router.get("/admin/tables")
async def fetch_tables():
    tables = __all__
    for i in tables:
        if i in [
            "BaseModel",
            "course_categories",
            "LessonTypeEnum",
            "LessonStatusEnum",
        ]:
            tables.remove(i)
    return {"tables": tables}


@admin_router.get("/admin/tables/{table}/records")
async def fetch_records(table: str):
    module = importlib.import_module(f"src.models")
    ResolvedClass = getattr(module, table)
    session = SessionLocal()
    records = session.query(ResolvedClass).all()
    session.close()
    return {"records": records}


@admin_router.get("/admin/tables/{table}/records/{id}")
async def fetch_record(table: str, id: int):
    module = importlib.import_module(f"src.models")
    ResolvedClass = getattr(module, table)
    session = SessionLocal()
    record = session.query(ResolvedClass).filter(ResolvedClass.id == id).first()
    session.close()
    return {"record": record}


@admin_router.delete("/admin/tables/{table}/records/{id}")
async def delete_record(table: str, id: int):
    module = importlib.import_module(f"src.models")
    ResolvedClass = getattr(module, table)
    session = SessionLocal()
    record = session.query(ResolvedClass).filter(ResolvedClass.id == id).first()
    session.delete(record)
    session.commit()
    session.close()
    return {"record": record}


@admin_router.put("/admin/tables/{table}/records/{id}")
async def update_record(table: str, id: int, data: dict):
    module = importlib.import_module(f"src.models")
    ResolvedClass = getattr(module, table)
    session = SessionLocal()
    record = session.query(ResolvedClass).filter(ResolvedClass.id == id).first()
    for key, value in data.items():
        if key == "lesson_type":
            value = LessonTypeEnum(value)

        if key == "lesson_status":
            value = LessonStatusEnum(value)

        setattr(record, key, value)
    session.commit()
    session.refresh(record)
    session.close()
    return {"record": record}


@admin_router.post("/admin/tables/{table}/records")
async def create_record(table: str, data: dict):
    module = importlib.import_module(f"src.models")
    ResolvedClass = getattr(module, table)
    if "id" in data:
        del data["id"]
    session = SessionLocal()
    record = ResolvedClass(**data)
    session.add(record)
    session.commit()
    session.refresh(record)
    session.close()
    return {"record": record}
