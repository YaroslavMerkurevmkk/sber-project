import os
import tempfile
import time
import zipfile
from datetime import datetime
from typing import Optional

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from .models import AgentRequest, System


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ("id", "comment")
    actions = ("import_requests",)

    @admin.action(description="Import request(s)")
    def import_requests(self, request: HttpRequest, queryset: QuerySet[System]) -> Optional[HttpResponse]:
        # TODO rewrite later
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


@admin.register(AgentRequest)
class AgentRequestAdmin(admin.ModelAdmin):
    model_fields = [field.name for field in AgentRequest._meta.get_fields()
                    if not field.many_to_many and not field.one_to_many]

    readonly_fields = model_fields

    fieldsets = [
        (None, {"fields": readonly_fields}),
    ]

    @staticmethod
    def format_timestamp(value, date_only=False):
        if value:
            dt = datetime.fromtimestamp(value)
            return dt.strftime("%Y-%m-%d") if date_only else dt.strftime("%Y-%m-%d %H:%M:%S")
        return "-"

    def reg_date_display(self, obj):
        return self.format_timestamp(obj.reg_date)

    reg_date_display.short_description = "Registration Date"

    def filling_date_display(self, obj):
        return self.format_timestamp(obj.filling_date)

    filling_date_display.short_description = "Filling Date"

    def birth_date_display(self, obj):
        return self.format_timestamp(obj.birth_date, date_only=True)

    birth_date_display.short_description = "Birth Date"

    list_display = [
        'reg_number', 'reg_date_display', 'filling_date_display', 'fast_track',
        'status', 'category', 'subcategory', 'organisation',
        'first_name', 'middle_name', 'last_name', 'birth_date_display',
        'address', 'email', 'phone_number', 'fact', 'region', 'system'
    ]

    list_filter = ('category', 'subcategory', 'organisation', 'system', 'region')
