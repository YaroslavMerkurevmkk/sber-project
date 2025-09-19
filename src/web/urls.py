from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('chat/', include('front.urls')),
    path('admin/', admin.site.urls),
]
