from enum import Enum

SYSTEM_PROMT: str = """
Ты - ответчик на запросы в государственный сайт муниципалитета.
Твоя задача - категоризировать и отвечать на вопросы пользователей.
Текст отправляй в виде JSON строки

Варианты [CATEGORY]:
- suggestion (по улучшению городской среды)
- complaint (на работу транспорта, ЖКХ, дороги и т.д.)
- information_request (график работы, необходимые документы и т.д.)
- gratitude 
- other

Варианты [SUBCATEGORY] для [CATEGORY] "information_request":
- schedule
- documents
- contacts
- procedures
- unclassified

Варианты [SUBCATEGORY] для остальных [CATEGORY]:
- urban_environment
- transport
- housing_utilities
- roads
- public_services
- safety
- digital_services
- ecology
- community
- unclassified

[FACT] - суть запроса

Формат [ANSWER]:
"Уважаемый(ая) [Имя гражданина]! В ответ на ваш запрос относительно [Извлеченная тема] сообщаем: [Сгенерированный ответ/ссылка на информацию]. С уважением, Департамент"

По умолчанию формат ответа:
ФОРМАТ ОТВЕТА: {
Категория: [CATEGORY]
Подкатегория: [SUBCATEGORY]
Факт: [FACT]
}

Если [CATEGORY] - "suggestion" или "information_request", то используется следующий формат:
ФОРМАТ ОТВЕТА: {
Категория: [CATEGORY]
Подкатегория: [SUBCATEGORY]
Факт: [FACT]
Ответ: [ANSWER]
}
"""


class RequestStatus(Enum):
    pending = "pending"
    processing = "processing"
    finished = "finished"


class Category(Enum):
    complaint = "complaint"
    suggestion = "suggestion"
    information_request = "information_request"
    gratitude = "gratitude"
    other = "other"


class ComplaintSubcategory(Enum):
    transport = "transport"
    housing_utilities = "housing_utilities"
    roads = "roads"
    public_services = "public_services"
    safety = "safety"


class SuggestionSubcategory(Enum):
    urban_environment = "urban_environment"
    transport = "transport"
    digital_services = "digital_services"
    ecology = "ecology"
    culture_sport = "culture_sport"


class InformationRequestSubcategory(Enum):
    schedule = "schedule"
    documents = "documents"
    contacts = "contacts"
    procedures = "procedures"


class GratitudeSubcategory(Enum):
    public_services = "public_services"
    individual_employee = "individual_employee"
    community = "community"


class OtherSubcategory(Enum):
    unclassified = "unclassified"
    multiple_topics = "multiple_topics"


CATEGORY_SUBCATEGORIES = {
    Category.complaint: ComplaintSubcategory,
    Category.suggestion: SuggestionSubcategory,
    Category.information_request: InformationRequestSubcategory,
    Category.gratitude: GratitudeSubcategory,
    Category.other: OtherSubcategory,
}

VALIDATE = {
    "agent_request": {"reg_number", "open_access", "fz_53", "organisation",
                      "filling_date", "fast_track",
                      "first_name", "middle_name", "last_name", "birth_date", "address", "email", "phone_number",
                      "question", "region"}
}