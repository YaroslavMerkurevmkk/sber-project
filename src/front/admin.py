from django.contrib import admin

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat")
