from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.core.repository import BaseSQLAlchemyRepository, TModelId

from .models import Enterprise, Organization


class EnterpriseRepository(BaseSQLAlchemyRepository[Enterprise]):
    async def get_enterprise_detailed(self, pk: TModelId) -> Enterprise:
        return (
            (
                await self.session.execute(
                    select(self.model).options(joinedload(self.model.organizations)).where(self.model.id == pk)
                )
            )
            .unique()
            .scalar_one_or_none()
        )


class OrganizationRepository(BaseSQLAlchemyRepository[Organization]): ...
