from __future__ import annotations

import json
from enum import Enum
from typing import Any


class MT(Enum):
    Command = "command"
    Data = "data"
    Notification = "notification"


class DT(Enum):
    Chats = "chats"
    NewChat = "new_chat"
    AiResponse = "ai_response"
    Messages = "messages"
    DeletedChat = "deleted_chat"


class CA(Enum):
    CreateChat = "create_chat"
    DeleteChat = "delete_chat"
    CreateMessage = "create_message"
    GetMessages = "get_messages"


class AlertType(Enum):
    Success = "success"
    Warning = "warning"
    Info = "info"
    Question = "question"
    Error = "error"


class Command:
    _action: CA = None
    _data: dict[str, Any] = None

    def __init__(self, payload: dict[str, Any]):
        self._action = CA(payload["action"])
        self._data = payload

    @property
    def action(self) -> CA:
        return self._action

    def __iter__(self):
        for key, value in self._data.items():
            yield key, value

    def __getitem__(self, item: str):
        return self._data[item]


class WsMessage:
    _m_type: MT = None
    _payload: dict[str, Any] = None

    def __init__(self, message_type: MT, payload: dict[str, Any]):
        self._m_type = message_type
        self._payload = payload

    @property
    def m_type(self) -> MT:
        return self._m_type

    @property
    def payload(self) -> dict[str, Any]:
        return self._payload

    @property
    def to_text_data(self) -> str:
        return json.dumps(dict(self))

    def __iter__(self):
        yield "type", self._m_type.value
        yield "payload", self._payload

    @staticmethod
    def from_dict(data: dict[str, Any]) -> WsMessage:
        mt = MT(data["type"])
        return WsMessage(mt, data["payload"])

    @staticmethod
    def from_command(command: Command) -> WsMessage:
        return WsMessage(MT.Command, dict(command))
