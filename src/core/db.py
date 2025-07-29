from rodi import ActivationScope
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.core.settings import Settings

Base = declarative_base()
metadata = Base.metadata


def session_factory(context: ActivationScope) -> AsyncSession:
    sessionmaker = context.provider.get(async_sessionmaker[AsyncSession])
    return sessionmaker()


def sessionmaker_factory(context: ActivationScope) -> async_sessionmaker[AsyncSession]:
    engine = context.provider.get(AsyncEngine)
    return async_sessionmaker(bind=engine, expire_on_commit=False)


def engine_factory(context: ActivationScope) -> AsyncEngine:
    settings: Settings = context.provider.get("settings")
    if not settings.connection_string:
        raise TypeError("Either pass a connection_string or an instance of sqlalchemy.ext.asyncio.AsyncEngine")
    return create_async_engine(
        url=settings.connection_string,
        future=True,
        query_cache_size=1200,
        pool_size=100,
        max_overflow=200,
        echo=True,
        echo_pool=True,
    )
