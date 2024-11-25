import os
from settings.base_settings import Settings


def get_settings() -> Settings:
    current_setting = Settings()
    try:
        if "PRODUCTION" in os.environ:
            from settings.prod_settings import ProductionSettings

            current_setting = ProductionSettings()

        elif "PRE_PRODUCTION" in os.environ:
            from settings.pre_production_settings import PreProductionSettings

            current_setting = PreProductionSettings()
        else:
            from settings.local import LocalSettings

            current_setting = LocalSettings()
        return Settings()
    except ImportError as err:
        print("Error while loading settings: %s", err)

        return current_setting


SETTINGS = get_settings()
