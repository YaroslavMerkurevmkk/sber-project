import json

from channels.generic.websocket import AsyncWebsocketConsumer

from core.models import WsMessage, MT, Command, CA, AlertType
from core.db import DatabaseApi
from front.models import MessageAuthor


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        await self.accept()

        chats = await DatabaseApi.get_user_chats(user)
        await self.send(text_data=WsMessage(MT.Data, payload={"chats": chats}).to_text_data)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        try:
            json_data = json.loads(text_data)
            message = WsMessage.from_dict(json_data)
            if message.m_type == MT.Command:
                await self._process_command(Command(message.payload))
                return

        except Exception as error:
            await self.send(WsMessage(MT.Notification, {
                "message": str(error),
                "result": AlertType.Error.value}).to_text_data)

    async def _process_command(self, command: Command) -> None:
        user = self.scope["user"]
        if command.action == CA.CreateChat:
            await DatabaseApi.create_chat(user, command["name"])
            await self.send(WsMessage(MT.Notification, {
                "message": "Chat created successfully",
                "result": AlertType.Success.value
            }).to_text_data)

        elif command.action == CA.CreateMessage:
            await DatabaseApi.create_message(user, command["chat_id"],
                                             command["content"], MessageAuthor.Human)
            # TODO ask AI agent

        elif command.action == CA.GetMessages:
            messages = await DatabaseApi.get_messages(command["chat_id"], command["last_ind"])
            await self.send(WsMessage(MT.Data, {
                "chat_id": command["chat_id"],
                "messages": messages
            }).to_text_data)
