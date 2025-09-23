import json

from channels.generic.websocket import AsyncWebsocketConsumer

from core.db import DatabaseApi
from core.models import WsMessage, MT, Command, CA, AlertType, DT
from front.models import MessageAuthor


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        await self.accept()

        chats = await DatabaseApi.get_user_chats(user)
        await self.send(WsMessage(MT.Data, payload={
            "data_type": DT.Chats.value,
            "chats": chats
        }).to_text_data)

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
            new_chat_base_info = await DatabaseApi.create_chat(user, command["name"])
            await self.send(WsMessage(MT.Data, {
                "data_type": DT.NewChat.value,
                "chat": new_chat_base_info
            }).to_text_data)

        elif command.action == CA.CreateMessage:
            some_ai_response = "Hello world!"

            chat_id = command["chat_id"]
            await DatabaseApi.create_message(user, chat_id,
                                             command["content"], MessageAuthor.Human)
            await DatabaseApi.create_message(user, chat_id,
                                             some_ai_response,
                                             MessageAuthor.Agent)

            await self.send(WsMessage(MT.Data, payload={
                "data_type": DT.AiResponse.value,
                "chat_id": chat_id,
                "content": some_ai_response
            }).to_text_data)

        elif command.action == CA.GetMessages:
            chat_id = command["chat_id"]
            messages = await DatabaseApi.get_messages(chat_id, command["last_ind"])
            await self.send(WsMessage(MT.Data, {
                "data_type": DT.Messages.value,
                "chat_id": chat_id,
                "messages": messages
            }).to_text_data)
