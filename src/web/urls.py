from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import front.views


urlpatterns = [
    path("", front.views.index, name="chat"),
    path("register/", front.views.register_view, name="register"),
    path("login/", front.views.login_view, name="login"),
    path("logout/", front.views.logout_view, name="logout"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)