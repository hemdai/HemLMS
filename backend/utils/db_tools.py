from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from utils.base import SessionLocal
from typing import Any, Union


def add_model_records(
    model: Any,
    data: Union[dict, Any],
    session: SessionLocal = None,
    sesson_close: bool = True,
):
    if not session:
        session = SessionLocal()
    try:
        if isinstance(data, dict):
            model_instance = model(**data)
        else:
            model_instance = data
        if isinstance(model_instance, list):
            session.add_all(model_instance)
            session.commit()
            for instance in model_instance:
                session.refresh(instance)
        else:
            session.add(model_instance)
            session.commit()
            session.refresh(model_instance)
        if sesson_close:
            session.close()
            return model_instance
        return model_instance, session
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
