from __future__ import annotations

from typing import Any

from asgiref.sync import sync_to_async

from front.models import Chat


class DatabaseApi:

    @staticmethod
    async def get_user_chats(user) -> list[dict[str, Any]]:
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
