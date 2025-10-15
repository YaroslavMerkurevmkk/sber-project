import json
from functools import wraps
from logging import getLogger
from typing import Optional, Any, Callable

from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.agent import GlobalAsyncAgent
from core.constants import RequestStatus, Category, SuggestionSubcategory, VALIDATE
from core.db import DatabaseApi
from front.models import System

logger = getLogger("front")


def get_json(request: ASGIRequest) -> Optional[dict[str, Any]]:
    return json.loads(request.body)



def post(func: Callable[[System, dict[str, Any]], Any]):
    @wraps(func)
    async def wrapper(request: ASGIRequest) -> JsonResponse:
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)
        try:
            data = get_json(request)
            if "token" not in data:
                return JsonResponse({"error": "Need token for use API"}, status=400)
            user = await DatabaseApi.get_system(data["token"])
            if not user:
                return JsonResponse({"error": "Invalid token"}, status=400)

            required_fields = VALIDATE[func.__name__]
            fields = set(data.keys())
            if required_fields.intersection(fields) != required_fields:
                skipped_fields = ", ".join(required_fields.difference(fields))
                return JsonResponse({"error": f"Skipped required fields: {skipped_fields}"}, status=400)

        except Exception as e:
            logger.exception(f"[post] Invalid JSON data", exc_info=e)
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        return await func(user, data)

    return wrapper


@csrf_exempt
@post
async def agent_request(system: System, data: dict[str, Any]) -> JsonResponse:
    answer = await GlobalAsyncAgent.process_request(data["question"])
    status = RequestStatus.pending.value
    category = Category.complaint.value
    subcategory = SuggestionSubcategory.ecology.value
    await DatabaseApi.save_request(data, answer, system, status, category, subcategory)
    return JsonResponse({"answer": answer})
