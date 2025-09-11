# catalog/models.py
from __future__ import annotations

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Модель категории товара.
    """
    name = models.CharField("Название", max_length=150, unique=True)
    slug = models.SlugField("Слаг", max_length=160, unique=True, blank=True)
    description = models.TextField("Описание", blank=True, default="")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self) -> str:
        # Человекочитаемое имя в админке и шаблонах
        return self.name

    def save(self, *args, **kwargs) -> None:
        """
        Автогенерация слага при отсутствии.
        Поддержка кириллицы через allow_unicode=True.
        """
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Модель товара.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField("Слаг", max_length=220, unique=True, blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, default=0)
    description = models.TextField("Описание", blank=True, default="")
    image = models.ImageField("Изображение", upload_to="products/", blank=True, null=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        """
        Автогенерация слага при отсутствии.
        Поддержка кириллицы через allow_unicode=True.
        """
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
