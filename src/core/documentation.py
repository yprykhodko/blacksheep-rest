import inspect
from typing import Any

import msgspec.json
from blacksheep.server.openapi.v3 import OpenAPIHandler, PydanticModelTypeHandler
from msgspec import Struct
from openapidocs.v3 import Info


def _try_is_subclass(object_type: type, check_type: type) -> bool:
    try:
        return issubclass(object_type, check_type)
    except TypeError:
        return False


class MsgspecStructTypeHandler(PydanticModelTypeHandler):
    def handles_type(self, object_type: type) -> bool:
        return Struct is not ... and inspect.isclass(object_type) and _try_is_subclass(object_type, Struct)

    def _get_object_schema(self, object_type: type) -> dict[str, Any]:
        return msgspec.json.schema(object_type)


docs = OpenAPIHandler(info=Info(title="Empower Frontdoor Service", version="0.0.1"), anonymous_access=True)
docs.include = lambda path, _: path.startswith("/api/")
docs.object_types_handlers.append(MsgspecStructTypeHandler())
