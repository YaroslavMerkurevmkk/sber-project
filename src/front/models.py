import time

import jwt
from django.conf import settings
from django.db import models


class User(models.Model):
    token = models.CharField("Token", max_length=128, default=jwt.encode(
        {"time": time.time()},
        getattr(settings, "SECRET_KEY", "apfisongr*&&*^awd8^&idiua"),
        algorithm="HS256"))
    comment = models.TextField("Comment", null=True)


class AgentRequest(models.Model):
    question = models.TextField("Question", null=False)
    answer = models.TextField("Answer", null=False)

    user = models.ForeignKey(User, related_name="requests", on_delete=models.CASCADE, verbose_name="User")

    def __iter__(self):
        yield "question", self.question
        yield "answer", self.answer

    def __str__(self):
        return self.question[:20]
