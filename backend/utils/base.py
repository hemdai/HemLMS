from sqlalchemy.ext.declarative import declarative_base
from typing import Any, Union
from settings import SETTINGS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

BaseModel = declarative_base()

DATABSE_URL = SETTINGS.db_url
engine = create_engine(DATABSE_URL, pool_size=SETTINGS.db_pool_size, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Any:
    db_connection = SessionLocal()
    try:
        yield db_connection
    except Exception as err:
        db_connection.rollback()
        raise err
    finally:
        db_connection.close()


def add_model_records(
    model: Any,
    data: Union[dict, Any],
    session: SessionLocal = None,
):
    if not session:
        session = SessionLocal()
    try:
        if isinstance(data, dict):
            model_instance = model(**data)
        else:
            model_instance = data
        session.add(model_instance)
        session.commit()
        session.refresh(model_instance)
        session.close()
        fresh_record = model_instance
        return fresh_record
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
