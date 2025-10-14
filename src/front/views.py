import json
from functools import wraps
from typing import Optional, Any, Callable

from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


async def get_json(request: ASGIRequest) -> Optional[dict[str, Any]]:
    try:
        body = await request.body
        return json.loads(body)
    except Exception as e:
        print("JSON parse error:", e)
        return None


def post(func: Callable[[ASGIRequest], Any]):
    @wraps(func)
    async def wrapper(request: ASGIRequest) -> JsonResponse:
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)
        return await func(request)
    return wrapper


@csrf_exempt
@post
async def agent_request(request: ASGIRequest) -> JsonResponse:
    data = await get_json(request)
    print("Parsed JSON:", data)

    return JsonResponse({"result": True})
