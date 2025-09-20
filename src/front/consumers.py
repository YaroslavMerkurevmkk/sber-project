import json

from channels.generic.websocket import AsyncWebsocketConsumer

from core.models import WsMessage, MT, Command, CA
from core.db import DatabaseApi


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        print("CONSUMER", user)
        if not user.is_authenticated:
            await self.close()
            return

        await self.accept()

        chats = await DatabaseApi.get_user_chats(user)
        await self.send(text_data=WsMessage(MT.Data, payload={"chats": chats}).to_text_data)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        json_data = json.loads(text_data)
        message = WsMessage.from_dict(json_data)
        if message.m_type == MT.Command:
            await self._process_command(Command(message.payload))
            return

        content = message.payload["content"]
        chat_id = message.payload["chat_id"]
        user = self.scope["user"]
        print(content, chat_id, user)
        # TODO add response from AI (async)
        ai_response = "Hello"

        await self.send(
            {
                'type': 'chat_message',
                'message': ai_response
            }
        )

    async def _process_command(self, command: Command) -> None:
        if Command.action == CA.CreateChat:
            user = self.scope["user"]
