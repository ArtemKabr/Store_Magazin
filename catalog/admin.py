# catalog/admin.py
"""Регистрация моделей в админ-панели."""
from django.contrib import admin
from .models import Category, Product, ContactInfo

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Админка контактных данных."""
    list_display = ("email", "phone", "address", "working_hours")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки отображения категорий в админке."""
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройки отображения товаров в админке."""
    list_display = ("id", "title", "category", "price", "is_published", "created_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)
    list_editable = ("is_published",)
    list_select_related = ("category",)


