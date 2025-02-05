from settings.base_settings import BasicSettings
import os


def get_settings():
    # Define different env settings logic here
    settings = BasicSettings()
    if "PROD" in os.environ:
        from settings.prod_settings import ProdSettings

        settings = ProdSettings()
    elif "PREPROD" in os.environ:
        from settings.pre_prod_settings import PreProdSettings

        settings = PreProdSettings
    return settings


SETTINGS = get_settings()
