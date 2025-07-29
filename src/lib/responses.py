from typing import TypeVar

from blacksheep import Content, Response
from msgspec.json import Encoder


T = TypeVar("T")
json_encoder = Encoder()


class StructResponse[T](Response):
    def __init__(
        self,
        data: T | None = None,
        status: int = 200,
        headers: list[tuple[bytes, bytes]] | None = None,
    ) -> None:
        super().__init__(
            status=status,
            headers=headers,
            content=Content(
                content_type=b"application/json",
                data=json_encoder.encode(data),
            ),
        )
