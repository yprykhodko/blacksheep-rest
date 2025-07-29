from uuid import UUID

from src.core.schemas import BaseStruct


class OrganizationCreateStruct(BaseStruct):
    display_name: str | None
    identifier: str


class OrganizationResponseStruct(BaseStruct):
    id: UUID
    display_name: str | None
    identifier: str
    enterprise_id: UUID


class OrganizationUpdateStruct(BaseStruct):
    display_name: str | None = None
    identifier: str | None = None
    enterprise_id: UUID | None = None
