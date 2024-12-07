from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from typing import Any


class Settings(BaseSettings):
    SECRETS: dict[str, str] = {}
    # Database
    postgres_db_name: str = SECRETS.get("POSTGRES_DB", "db_hemlms")
    postgres_db_user: str = SECRETS.get("POSTGRES_USER", "db_hemlms")
    postgres_db_password: str = SECRETS.get("POSTGRES_PASSWORD", "user_hemlms")
    postgres_db_host: str = SECRETS.get("POSTGRES_HOST", "postgres")
    postgres_db_port: int = SECRETS.get("POSTGRES_PORT", "5432")
    db_pool_size: int = 20

    @property
    def db_url(self) -> Any:
        url = PostgresDsn.build(
            scheme="postgresql",
            username=self.postgres_db_user,
            password=self.postgres_db_password,
            host=self.postgres_db_host,
            port=self.postgres_db_port,
            path=self.postgres_db_name,
        )
        return url.unicode_string()
