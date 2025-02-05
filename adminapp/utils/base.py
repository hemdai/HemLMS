from sqlalchemy.ext.declarative import declarative_base
from settings import SETTINGS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BaseModel = declarative_base()

DATABASE_URL = SETTINGS.db_url
engine = create_engine(
    DATABASE_URL, pool_size=SETTINGS.db_pool_size, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db_connection = SessionLocal()
    try:
        yield db_connection
    except Exception as err:
        db_connection.rollback()
        raise err
    finally:
        db_connection.close()
