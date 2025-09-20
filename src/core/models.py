import json
from enum import Enum
from typing import Any


class MT(Enum):
    Command = "command"
    Data = "data"


class CT(Enum):
    Init = "init"


class Command:
    _c_type: CT = None
    _data: dict[str, Any] = None

    def __init__(self, payload: dict[str, Any]):
        self._c_type = CT(payload["c_type"])
        self._data = payload

    @property
    def type(self) -> CT:
        return self._c_type

    def __getitem__(self, item: str, default: Any):
        return self._data.get(item, default)


class WsMessage:
    _m_type: MT = None
    _payload: dict[str, Any] = None

    def __init__(self, text_data: str):
        data = json.loads(text_data)
        self._m_type = MT(data["type"])
        self._payload = data["payload"]

    @property
    def m_type(self) -> MT:
        return self._m_type

    @property
    def payload(self) -> dict[str, Any]:
        return self._payload
