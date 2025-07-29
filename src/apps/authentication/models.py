import uuid

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    issuer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    realm: Mapped[str | None] = mapped_column(String(255), nullable=True)
    aad_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean(), default=False)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_login: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)
