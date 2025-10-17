"""Сервисные функции для работы с продуктами."""

from catalog.models import Category, Product


def get_products_by_category(slug: str):
    """Возвращает все опубликованные продукты выбранной категории."""
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return []
    return Product.objects.filter(category=category, is_published=True)
