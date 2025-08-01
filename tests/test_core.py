from blacksheep import Application

from src.core.settings import Settings, load_settings
from src.main import configure_application


def test_settings_return_settings() -> None:
    assert isinstance(load_settings(), Settings)


def test_configure_application() -> None:
    assert isinstance(configure_application(load_settings()), Application)
