from typing import Any

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class MessageAuthor(models.IntegerChoices):
    Agent = (0, "Agent")
    Human = (1, "Human")


class Chat(models.Model):
    name = models.CharField("Name", max_length=100, null=False)
    user = models.ForeignKey(User, related_name="chats", on_delete=models.CASCADE, verbose_name="User")

    @property
    def base_info(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name
        }

    def __iter__(self):
        yield "id", self.id
        yield "name", self.name
        yield "messages", [dict(message) for message in self.messages.all()]

    def __str__(self):
        return self.name


class Message(models.Model):
    content = models.TextField("Content", null=False)
    author = models.IntegerField("Author", choices=MessageAuthor.choices, null=False)
    links = models.TextField("Links", null=True, default=None)

    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE, verbose_name="Chat")

    def to_ai_message(self) -> dict[str, str]:
        return {
            "role": "user" if self.author == MessageAuthor.Human.value else "assistant",
            "content": self.content
        }

    def __iter__(self):
        yield "id", self.id
        yield "content", self.content
        yield "author", self.author
        yield "links", self.links

    def __str__(self):
        return self.content[:20]
