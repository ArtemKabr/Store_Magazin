# catalog/admin.py
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для товаров."""
    # Было: list_display = ("id", "name", "category", "price", "is_published", "created_at")
    list_display = ("id", "title", "category", "price", "is_published", "created_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "slug", "description")
    # Было: {"slug": ("name",)}
    prepopulated_fields = {"slug": ("title",)}
