import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class Enterprise(Base):
    __tablename__ = "enterprise"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    identifier: Mapped[str] = mapped_column(String(255), unique=True)
    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="enterprise", lazy="joined", cascade="all, delete-orphan"
    )


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    display_name: Mapped[str] = mapped_column(String(255))
    identifier: Mapped[str] = mapped_column(String(255), unique=True)
    enterprise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enterprise.id"))
    enterprise: Mapped["Enterprise"] = relationship(back_populates="organizations")
    environments: Mapped["Environment"] = relationship(back_populates="organization", cascade="all, delete-orphan")


class Environment(Base):
    __tablename__ = "environment"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    display_name: Mapped[str] = mapped_column(String(255))
    identifier: Mapped[str] = mapped_column(String(255), unique=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["Organization"] = relationship(back_populates="environments")
