from uuid import UUID

from blacksheep import Response
from blacksheep.server.controllers import APIController, delete, get, patch, post
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.lib.binders import FromStruct
from src.lib.responses import StructResponse

from .models import Enterprise, Organization
from .repository import EnterpriseRepository, OrganizationRepository
from .schemas import (
    EnterpriseCreateStruct,
    EnterpriseDetailResponseStruct,
    EnterpriseResponseStruct,
    EnterpriseUpdateStruct,
    OrganizationCreateStruct,
    OrganizationResponseStruct,
    OrganizationUpdateStruct,
)


class EnterpriseController(APIController):
    def __init__(self, session: AsyncSession, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = EnterpriseRepository(Enterprise, session)

    @classmethod
    def class_name(cls) -> str:
        return "enterprises"

    @get()
    async def list_enterprises(self) -> StructResponse[list[EnterpriseResponseStruct]]:
        enterprises = await self.repository.list()
        return StructResponse(data=[EnterpriseResponseStruct.from_model(enterprise) for enterprise in enterprises])

    @get("/{uuid:enterprise_id}")
    async def get_enterprise_by_id(self, enterprise_id: UUID) -> EnterpriseResponseStruct:
        enterprise = await self.repository.get(enterprise_id)
        return EnterpriseResponseStruct.from_model(enterprise)

    @get("/{uuid:enterprise_id}/detail")
    async def get_enterprise_by_id_detailed(
        self, enterprise_id: UUID
    ) -> StructResponse[EnterpriseDetailResponseStruct]:
        enterprise = await self.repository.get_enterprise_detailed(enterprise_id)
        return StructResponse(data=EnterpriseDetailResponseStruct.from_model(enterprise))

    @post()
    async def create_enterprise(
        self, data: FromStruct[EnterpriseCreateStruct]
    ) -> StructResponse[EnterpriseResponseStruct]:
        print(data)
        enterprise = await self.repository.create(data.value)
        return StructResponse(data=EnterpriseResponseStruct.from_model(enterprise))

    @delete("/{uuid:enterprise_id}")
    async def delete_enterprise(self, enterprise_id: UUID) -> Response:
        await self.repository.delete(enterprise_id)
        return self.no_content()

    @patch("/{uuid:enterprise_id}")
    async def update_enterprise(
        self, enterprise_id: UUID, data: EnterpriseUpdateStruct
    ) -> StructResponse[EnterpriseResponseStruct]:
        enterprise = await self.repository.update(data, enterprise_id)
        return StructResponse(data=EnterpriseResponseStruct.from_model(enterprise))


class OrganizationController(APIController):
    def __init__(self, session: AsyncSession, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session
        self.repository = OrganizationRepository(Organization, session)

    @classmethod
    def class_name(cls) -> str:
        return "organizations"

    @classmethod
    def route(cls) -> str | None:
        return "api/enterprises/{uuid:enterprise_id}/organizations"

    @get()
    async def list_organizations(self, enterprise_id: UUID) -> StructResponse[list[OrganizationResponseStruct]]:
        organizations = await self.repository.list(enterprise_id=enterprise_id)
        return StructResponse([OrganizationResponseStruct.from_model(org) for org in organizations])

    @get("/{uuid:organization_id}")
    async def get_organization_by_id(
        self, enterprise_id: UUID, organization_id: UUID
    ) -> StructResponse[OrganizationResponseStruct]:
        organization = await self.repository.get(organization_id, enterprise_id=enterprise_id)
        return StructResponse(OrganizationResponseStruct.from_model(organization))

    @post()
    async def create_organization(
        self,
        enterprise_id: UUID,
        data: FromStruct[OrganizationCreateStruct],
    ) -> StructResponse[OrganizationResponseStruct]:
        organization = await self.repository.create(data.value, enterprise_id=enterprise_id)
        return StructResponse(OrganizationResponseStruct.from_model(organization))

    @patch("/{uuid:organization_id}")
    async def update_organization(
        self, enterprise_id: UUID, organization_id: UUID, data: FromStruct[OrganizationUpdateStruct]
    ) -> StructResponse[OrganizationResponseStruct]:
        organization = await self.repository.update(data.value, organization_id, enterprise_id=enterprise_id)
        return StructResponse(OrganizationResponseStruct.from_model(organization))

    @delete("/{uuid:organization_id}")
    async def delete_organization(self, enterprise_id: UUID, organization_id: UUID) -> Response:
        await self.repository.delete(organization_id, enterprise_id=enterprise_id)
        return self.no_content()
