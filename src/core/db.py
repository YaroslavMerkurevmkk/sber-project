from __future__ import annotations

from logging import Logger, getLogger
from typing import Optional, Any, Dict

from asgiref.sync import sync_to_async

from core.constants import VALIDATE
from front.models import AgentRequest, System


class DatabaseApi:
    tag: str = "database-api"
    logger: Logger = getLogger("front")

    @staticmethod
    async def get_system(token: str) -> Optional[System]:
        try:
            return await sync_to_async(System.objects.filter(token=token).first)()
        except System.DoesNotExist:
            DatabaseApi.logger.warning(f"[{DatabaseApi.tag}] System ({token}) not found!")
        return None

    @staticmethod
    async def save_request(data: Dict[str, Any],
                           answer: str,
                           system: System,
                           status: str,
                           category: str,
                           subcategory: str,
                           fact: str) -> None:

        data_for_model = {}
        for field in VALIDATE["agent_request"]:
            data_for_model[field] = data[field]

        data_for_model["answer"] = answer
        data_for_model["system"] = system
        data_for_model["status"] = status
        data_for_model["category"] = category
        data_for_model["subcategory"] = subcategory
        data_for_model["fact"] = fact

        request_obj = AgentRequest(**data_for_model)
        await sync_to_async(request_obj.save)()
        DatabaseApi.logger.info(f"[{DatabaseApi.tag}] Saved request: {request_obj.id} for user: {system.id}")

    @staticmethod
    async def get_requests(system: System) -> list[dict[str, str]]:
        qs = await sync_to_async(system.requests.all)()
        return [dict(request) for request in qs]
