# catalog/management/commands/seed_products.py
from __future__ import annotations

from decimal import Decimal
from hashlib import md5
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from catalog.models import Category, Product

# путь к папке с изображениями
MEDIA_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "media" / "products"


def make_unique_slug(text: str, used: set[str]) -> str:
    """Генерация уникального slug (с поддержкой кириллицы)."""
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
    """Команда для очистки и наполнения БД тестовыми категориями и продуктами."""

    help = "Очищает таблицы Category и Product, " "добавляет тестовые записи с фото, если найдены в media/products."

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
            categories = [
                Category(
                    name=name,
                    slug=make_unique_slug(name, used_cat_slugs),
                    description=desc,
                )
                for name, desc in categories_data
            ]
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

                # === поиск изображения ===
                slug_name = slugify(title, allow_unicode=True)
                possible_files = list(MEDIA_ROOT.glob(f"{slug_name}.*"))
                image_path = None
                if possible_files:
                    image_path = f"products/{possible_files[0].name}"

                products.append(
                    Product(
                        title=title,
                        slug=make_unique_slug(title, used_prod_slugs),
                        price=price,
                        description=desc,
                        category=category,
                        is_published=True,
                        image=image_path,  # если найдено фото — привязываем
                    )
                )

            Product.objects.bulk_create(products)
            self.stdout.write(self.style.SUCCESS("✅ Готово! Тестовые данные и фото загружены."))
