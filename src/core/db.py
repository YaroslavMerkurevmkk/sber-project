from __future__ import annotations

from typing import Any

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from logging import Logger, getLogger

from core.constants import START_MESSAGE
from front.models import User, AgentRequest



class DatabaseApi:
    tag: str = "database-api"
    logger: Logger = getLogger("front")
