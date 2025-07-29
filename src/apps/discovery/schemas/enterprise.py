from uuid import UUID

from src.core.schemas import BaseStruct

from .organizations import OrganizationResponseStruct


class EnterpriseCreateStruct(BaseStruct):
    name: str | None
    identifier: str


class EnterpriseResponseStruct(BaseStruct):
    id: UUID
    name: str | None
    identifier: str


class EnterpriseUpdateStruct(BaseStruct):
    name: str | None = None
    identifier: str | None = None


class EnterpriseDetailResponseStruct(BaseStruct):
    id: UUID
    name: str | None
    identifier: str
    organizations: list[OrganizationResponseStruct] = []
