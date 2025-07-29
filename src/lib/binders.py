from struct import Struct
from typing import Any, TypeVar

import msgspec
from blacksheep import Request
from blacksheep.server.bindings import BodyBinder, BoundValue
from blacksheep.settings.json import json_settings


TMsgSpecStruct = TypeVar("TMsgSpecStruct", bound=Struct)


class FromStruct(BoundValue[TMsgSpecStruct]): ...


decoder = msgspec.msgpack.Decoder()


class MsgPackBinder(BodyBinder):
    handle = FromStruct

    @property
    def content_type(self) -> str:
        return "application/json"

    def matches_content_type(self, request: Request) -> bool:
        return request.declares_json()

    async def read_data(self, request: Request) -> Any:
        if not (content := await request.read()):
            return None
        return msgspec.json.decode(content, type=self.expected_type)


json_decoder = msgspec.json.Decoder()
json_settings.use(loads=json_decoder.decode)  # type: ignore[no-untyped-call]
