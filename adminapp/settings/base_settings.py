from pydantic import PostgresDsn
from typing import Any
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class BasicSettings(BaseSettings):
    pg_db_name: str = os.getenv("ADMIN_APP_POSTGRES_DB")
    pg_db_user: str = os.getenv("ADMIN_APP_POSTGRES_USER")
    pg_db_password: str = os.getenv("ADMIN_APP_POSTGRES_PASSWORD")
    pg_db_host: str = os.getenv("ADMIN_APP_POSTGRES_HOST")
    pg_db_port: int = 5432
    db_pool_size: int = 20

    @property
    def db_url(self) -> Any:
        url = PostgresDsn.build(
            scheme="postgresql",
            username=self.pg_db_user,
            password=self.pg_db_password,
            host=self.pg_db_host,
            port=self.pg_db_port,
            path=self.pg_db_name,
        )
        return url.unicode_string()
