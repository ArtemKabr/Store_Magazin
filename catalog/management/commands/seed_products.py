# catalog/management/commands/seed_products.py
from __future__ import annotations

from hashlib import md5
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from catalog.models import Category, Product


def make_unique_slug(text: str, used: set[str]) -> str:
    """
    Генерация уникального slug.
    - Поддержка кириллицы (allow_unicode=True)
    - Если slug пустой — берём md5-хэш
    - Проверяем уникальность внутри used
    """
    base = slugify(text, allow_unicode=True).strip()
    if not base:
        base = md5(text.encode("utf-8")).hexdigest()[:8]

    slug = base
    i = 1
    while slug in used:
        slug = f"{base}-{i}"
        i += 1
    used.add(slug)
    return slug


class Command(BaseCommand):
    """Кастомная команда для очистки и наполнения БД тестовыми категориями и продуктами."""

    help = "Очищает таблицы Category и Product, добавляет тестовые записи."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("🗑 Очищаем таблицы...")
            Product.objects.all().delete()
            Category.objects.all().delete()

            # === Категории ===
            categories_data = [
                ("Смартфоны", "Категория смартфонов"),
                ("Ноутбуки", "Категория ноутбуков"),
                ("Наушники", "Категория аудио-аксессуаров"),
            ]

            used_cat_slugs: set[str] = set()
            categories: list[Category] = []
            for name, desc in categories_data:
                categories.append(
                    Category(
                        name=name,
                        slug=make_unique_slug(name, used_cat_slugs),
                        description=desc,
                    )
                )
            Category.objects.bulk_create(categories)
            categories = list(Category.objects.all())

            # === Продукты ===
            products_data = [
                ("iPhone 14", Decimal("799.99"), "Смартфон Apple iPhone 14"),
                ("Samsung Galaxy S23", Decimal("749.00"), "Флагман Samsung"),
                ("MacBook Air 13", Decimal("1199.00"), "Ноутбук Apple M2"),
                ("ASUS ZenBook", Decimal("1099.00"), "Ультрабук ASUS"),
                ("AirPods Pro 2", Decimal("249.00"), "Наушники Apple"),
                ("Sony WH-1000XM5", Decimal("349.00"), "Наушники Sony"),
            ]

            used_prod_slugs: set[str] = set()
            products: list[Product] = []
            for idx, (title, price, desc) in enumerate(products_data):
                category = categories[idx % len(categories)]
                products.append(
                    Product(
                        title=title,
                        slug=make_unique_slug(title, used_prod_slugs),
                        price=price,
                        description=desc,
                        category=category,
                        is_published=True,
                    )
                )
            Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS("✅ Готово! Тестовые данные загружены."))

