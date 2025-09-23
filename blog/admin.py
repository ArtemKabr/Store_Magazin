# blog/admin.py
"""Регистрация моделей блога в админ-панели."""
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройки отображения статей в админке."""
    list_display = ("id", "title", "is_published", "views", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
