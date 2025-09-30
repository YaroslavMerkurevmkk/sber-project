import os
import tempfile
import time
import zipfile
from typing import Optional

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    actions = ("import_chat",)

    @admin.action(description="Import chat(s)")
    def import_chat(self, request: HttpRequest, queryset: QuerySet[Chat]) -> Optional[HttpResponse]:
        if queryset.count() == 0:
            self.message_user(request, "Select one or more chats.", level="error")
            return None

        if queryset.count() == 1:
            chat = queryset.first()
            response = HttpResponse(chat.to_import, content_type="application/json")
            response["Content-Disposition"] = f'attachment; filename="{chat.name}.json"'
            return response

        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
            zip_filename = temp_zip.name
            exist_filenames = []
            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                for chat in queryset:
                    filename = chat.name.replace(" ", "_")
                    if filename in exist_filenames:
                        filename += str(int(time.time() * 1000))
                    exist_filenames.append(filename)

                    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as temp_file:
                        temp_file.write(chat.to_import)
                        temp_file.flush()
                        temp_file.close()
                        zip_file.write(temp_file.name, f"{filename}.json")
                        os.unlink(temp_file.name)

        with open(zip_filename, "rb") as zip_file:
            response = HttpResponse(zip_file.read(), content_type="application/zip")
            response["Content-Disposition"] = 'attachment; filename="chats.zip"'
            os.unlink(zip_filename)
            return response

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat")
