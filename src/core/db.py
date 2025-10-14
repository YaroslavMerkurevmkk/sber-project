from __future__ import annotations

from logging import Logger, getLogger
from typing import Optional

from asgiref.sync import sync_to_async

from front.models import User, AgentRequest


class DatabaseApi:
    tag: str = "database-api"
    logger: Logger = getLogger("front")

    @staticmethod
    async def get_user(token: str) -> Optional[User]:
        try:
            return await sync_to_async(User.objects.filter(token=token).first)()
        except User.DoesNotExist:
            DatabaseApi.logger.warning(f"[{DatabaseApi.tag}] User ({token}) not found!")
        return None

    @staticmethod
    async def save_request(question: str,
                           answer: str,
                           user: User) -> None:
        request_obj = AgentRequest(
            question=question, answer=answer, user=user
        )
        await sync_to_async(request_obj.save)()
        DatabaseApi.logger.info(f"[{DatabaseApi.tag}] Saved request: {request_obj.id} for user: {user.id}")


    @staticmethod
    async def get_requests(user: User) -> list[dict[str, str]]:
        qs = await sync_to_async(user.messages.all)()
        return [dict(request) for request in qs]

