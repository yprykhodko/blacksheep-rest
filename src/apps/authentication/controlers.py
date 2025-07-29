from blacksheep.server.controllers import APIController, get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserController(APIController):
    @classmethod
    def class_name(cls) -> str:
        return "users"

    @get("/")
    async def get_users(self, session: AsyncSession) -> list[str]:
        users = (await session.scalars(select(User))).all()
        return [user.username for user in users]
