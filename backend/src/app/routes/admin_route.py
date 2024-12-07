# /admin/tables
from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags
from utils.base import SessionLocal
from src.models import __all__, LessonTypeEnum, LessonStatusEnum
import importlib
from src.app.admin import registry

admin_router = APIRouter(tags=[RouteTags.ACCOUNT])


@admin_router.get("/admin/tables")
async def fetch_tables():
    model_list = __all__
    removing_tables = [
        "BaseModel",
        "course_categories",
        "LessonTypeEnum",
        "LessonStatusEnum",
    ]
    new_model_list = list(set(model_list) - set(removing_tables))
    return {"tables": new_model_list}


@admin_router.get("/admin/tables/{table}/records")
async def fetch_records(table: str):
    module = importlib.import_module(f"src.models")
    ResolvedClass = getattr(module, table)
    session = SessionLocal()
    schema = registry.get(table)
    records = session.query(ResolvedClass).all()
    session.close()
    context = [schema.from_orm(record) for record in records]
    if context:
        return {"records": context}


@admin_router.get("/admin/tables/{table}/records/{id}")
async def fetch_record(table: str, id: int):
    module = importlib.import_module(f"src.models")
    ResolvedClass = getattr(module, table)
    session = SessionLocal()
    schema = registry.get(table)
    record = session.query(ResolvedClass).filter(ResolvedClass.id == id).first()
    session.close()
    context = schema.from_orm(record)
    return {"record": context}


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
    schema = registry.get(table)
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
    schema = registry.get(table)
    schema_object = schema(**data)
    session = SessionLocal()
    record = ResolvedClass(**dict(schema_object))
    session.add(record)
    session.commit()
    session.refresh(record)
    session.close()
    return {"record": record}
