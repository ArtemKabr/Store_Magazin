"""Корневые URL проекта: подключение URL приложения catalog через include."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),     # /admin/
    path("", include("catalog.urls")),   # 👈 все маршруты приложения catalog
]
