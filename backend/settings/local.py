from settings.base_settings import Settings


class LocalSettings(Settings):
    postgres_db_host: str = "localhost"
    postgres_db_port: str = "5432"
    postgres_db_name: str = "db_hemlms"
    postgres_db_user: str = "db_hemlms"
    postgres_db_user: str = "user_hemlms"
