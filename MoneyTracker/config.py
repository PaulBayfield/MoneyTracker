from sanic.config import Config


class AppConfig(Config):
    OAS = False

    FALLBACK_ERROR_FORMAT = "json"
