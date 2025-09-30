from __future__ import annotations

from typing import Any

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from logging import Logger, getLogger

from core.constants import START_MESSAGE
from front.models import Chat, Message, MessageAuthor

User = get_user_model()


class DatabaseApi:
    tag: str = "database-api"
    logger: Logger = getLogger("front")

    @staticmethod
    async def get_user_chats(user: User) -> list[dict[str, Any]]:
        result = await sync_to_async(
            lambda: [chat.base_info for chat in Chat.objects.filter(user=user).order_by("-id")]
        )()

        if not result:
            return result

        messages = await DatabaseApi.get_messages(result[0]["id"])
        result[0].update({"messages": messages})
        return result

    @staticmethod
    async def get_messages(chat_id: int, last_ind: int = -1) -> list[dict[str, Any]]:
        qs = await sync_to_async(
            lambda: Chat.objects.get(id=chat_id).messages.order_by("-id")
        )()

        if last_ind != -1:
            qs = qs.filter(id__lt=last_ind)

        qs = qs[:20]

        result = await sync_to_async(lambda: [dict(msg) for msg in reversed(qs)])()
        return result

    @staticmethod
    async def create_chat(user: User, name: str) -> dict[str, Any]:
        chat = Chat(user=user, name=name)
        await sync_to_async(chat.save)()
        await sync_to_async(Message(content=START_MESSAGE, author=MessageAuthor.Agent.value,
                                    links="", chat=chat).save)()
        DatabaseApi.logger.info(f"[{DatabaseApi.tag}] Created chat: {chat.id}")
        return chat.base_info

    @staticmethod
    async def rename_chat(user: User, chat_id: int, name: str) -> None:
        try:
            chat = await sync_to_async(Chat.objects.filter(user=user, id=chat_id).first)()
            chat.name = name
            await sync_to_async(chat.save)()
            DatabaseApi.logger.info(f"[{DatabaseApi.tag}] Renamed chat: {chat.id}")
        except Chat.DoesNotExist:
            raise ValueError("Chat not found!")

    @staticmethod
    async def create_message(user: User,
                             chat_id: int,
                             content: str,
                             author: MessageAuthor,
                             links: str = None) -> None:
        try:
            chat = await sync_to_async(Chat.objects.filter(user=user, id=chat_id).first)()
        except Chat.DoesNotExist:
            raise ValueError("Chat not found!")

        msg = Message(content=content, author=author.value,
                                    links=links, chat=chat)
        await sync_to_async(msg.save)()
        DatabaseApi.logger.info(f"[{DatabaseApi.tag}] Created message: {msg.id}")

    @staticmethod
    async def get_chat(user: User, chat_id: int) -> list[dict[str, str]]:
        qs = await sync_to_async(
            lambda: Chat.objects.get(id=chat_id, user=user).messages.all()
        )()
        result = await sync_to_async(lambda: [msg.to_ai_message() for msg in qs])()
        return result

    @staticmethod
    async def delete_chat(user: User, chat_id: int) -> None:
        await sync_to_async(lambda: Chat.objects.filter(user=user, id=chat_id).delete)()
