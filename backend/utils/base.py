from sqlalchemy.ext.declarative import declarative_base
from typing import Any, Union
from settings import SETTINGS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, UploadFile
from pathlib import Path
import shutil

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


def save_file(file: UploadFile, document_type: str) -> Union[str, None]:
    file_sub_dir = {
        "image": "image",
        "video": "video",
        "audio": "audio",
        "file": "file",
    }
    dir = f"{SETTINGS.BASE_UPLOAD_DIR}/{file_sub_dir[document_type]}"
    Path(dir).mkdir(parents=True, exist_ok=True)
    file_path = f"{dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path
