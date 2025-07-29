from rodi import Container
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from .db import engine_factory, session_factory, sessionmaker_factory
from .settings import Settings, load_settings


def configure_services() -> tuple[Container, Settings]:
    container = Container()
    settings = load_settings()

    container.add_instance(settings)

    container.add_singleton_by_factory(engine_factory, AsyncEngine)
    container.add_singleton_by_factory(sessionmaker_factory, async_sessionmaker[AsyncSession])
    container.add_scoped_by_factory(session_factory, AsyncSession)
    container.add_alias("db_session", AsyncSession)

    return container, settings
