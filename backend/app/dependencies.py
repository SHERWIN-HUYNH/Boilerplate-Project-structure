from collections.abc import Generator

from app.core.config import Settings, get_settings


def get_app_settings() -> Settings:
    return get_settings()


def get_db() -> Generator[None, None, None]:
    yield
