from sqlalchemy.ext.declarative import declarative_base
from typing import Any
from settings import SETTINGS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
