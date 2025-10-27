import time

import jwt
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.constants import RequestStatus, Category, CATEGORY_SUBCATEGORIES


def generate_token():
    return jwt.encode(
        {"time": time.time()},
        getattr(settings, "SECRET_KEY", "apfisongr*&&*^awd8^&idiua"),
        algorithm="HS256",
    )


class System(models.Model):
    token = models.CharField("Token", max_length=128, default=generate_token)
    comment = models.TextField("Comment", null=True, blank=True)

    def __str__(self):
        return self.comment[:30] if self.comment else "No comment"


class AgentRequest(models.Model):
    STATUS_CHOICES = [(pt.value, pt.value) for pt in RequestStatus]
    CATEGORY_CHOICES = [(pt.value, pt.value) for pt in Category]
    SUBCATEGORY_CHOICES = [
        (pt.value, pt.value)
        for enum_cls in CATEGORY_SUBCATEGORIES.values()
        for pt in enum_cls
    ]

    reg_number = models.IntegerField("Registration number", unique=True)
    reg_date = models.BigIntegerField("Registration date", default=int(time.time()))
    open_access = models.BooleanField("Open access", default=False)
    fz_53 = models.BooleanField("59-FZ", default=False)

    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES)
    category = models.CharField("Category", max_length=30, choices=CATEGORY_CHOICES)
    subcategory = models.CharField("Subcategory", max_length=30, choices=SUBCATEGORY_CHOICES)

    fact = models.TextField("Fact")
    organisation = models.CharField("Organisation", max_length=300)

    filling_date = models.BigIntegerField("Filling date", default=int(time.time()))
    fast_track = models.BooleanField("Fast track", default=False)

    first_name = models.CharField("First name", max_length=200)
    middle_name = models.CharField("Middle name", max_length=200)
    last_name = models.CharField("Last name", max_length=200)
    birth_date = models.BigIntegerField("Birth date")
    address = models.TextField("Address", max_length=200)
    email = models.EmailField("Email")
    phone_number = models.CharField("Phone", max_length=30, blank=True, null=True)

    question = models.TextField("Question")
    region = models.TextField("Region")
    answer = models.TextField("Answer", blank=True, null=True)

    system = models.ForeignKey(System, related_name="requests", on_delete=models.CASCADE, verbose_name="System")

    def clean(self):
        super().clean()
        if self.category and self.subcategory:
            sub_enum = CATEGORY_SUBCATEGORIES.get(Category(self.category))
            if sub_enum:
                valid_subcategories = [pt.value for pt in sub_enum]
                if self.subcategory not in valid_subcategories:
                    raise ValidationError({
                        "subcategory": f"Subcategory '{self.subcategory}' does not correspond to category '{self.category}'."
                    })

    def __iter__(self):
        for field in self._meta.fields:
            field_name = field.name
            value = getattr(self, field_name)
            yield field_name, value

    def __str__(self):
        return self.question[:20] if self.question else "No question"
