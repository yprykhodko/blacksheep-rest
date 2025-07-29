from typing import Any, Self, TypeVar

from msgspec import Struct
from sqlalchemy.orm import DeclarativeBase


TModel = TypeVar("TModel", bound=DeclarativeBase)


class BaseStruct(Struct):
    @classmethod
    def from_model(cls, model: TModel, **kwargs: Any) -> "BaseStruct":
        return cls(**{f: getattr(model, f) for f in cls.__struct_fields__}, **kwargs)

    def to_model(self, model_class: type[TModel], **kwargs: Any) -> TModel:
        return model_class(**self.to_dict(), **kwargs)

    def to_dict(self) -> dict[str, Any]:
        return {f: getattr(self, f) for f in self.__struct_fields__}
