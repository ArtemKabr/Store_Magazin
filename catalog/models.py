from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ContactInfo(models.Model):
    """
    Контактные данные магазина (редактируются через админку).
    """
    email = models.EmailField("Email", blank=True, default="")
    phone = models.CharField("Телефон", max_length=50, blank=True, default="")
    address = models.CharField("Адрес", max_length=255, blank=True, default="")
    working_hours = models.CharField("Время работы", max_length=255, blank=True, default="")
    map_embed = models.TextField("Карта (iframe)", blank=True, default="")

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self) -> str:
        """Возвращаем человекочитаемое имя записи."""
        return self.email or self.phone or "Контакты"


class Category(models.Model):
    """
    Категория товара.
    """
    name = models.CharField("Название", max_length=150, unique=True)
    slug = models.SlugField("Слаг", max_length=160, unique=True, blank=True)
    description = models.TextField("Описание", blank=True, default="")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self) -> str:
        """Имя категории в админке/шаблонах."""
        return self.name

    def save(self, *args, **kwargs) -> None:
        """
        Автогенерация слага при отсутствии.
        Поддержка кириллицы через allow_unicode=True.
        """
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """
        URL страницы категории.
        Используйте, если в urls есть именованный маршрут 'catalog:category'.
        """
        return reverse("catalog:category", kwargs={"slug": self.slug})


class Product(models.Model):
    """
    Товар каталога.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField("Слаг", max_length=220, unique=True, blank=True)
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],  # цена не может быть отрицательной
    )
    description = models.TextField("Описание", blank=True, default="")
    image = models.ImageField("Изображение", upload_to="products/", blank=True, null=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-created_at",)
        # Индексы под частые выборки/сортировки: главная страница, фильтр по категории
        indexes = [
            models.Index(fields=("is_published", "-created_at"), name="prod_pub_created_idx"),
            models.Index(fields=("category", "is_published"), name="prod_cat_pub_idx"),
        ]

    def __str__(self) -> str:
        """Имя товара в админке/шаблонах."""
        return self.title

    def save(self, *args, **kwargs) -> None:
        """
        Автогенерация слага при отсутствии.
        Поддержка кириллицы через allow_unicode=True.
        """
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """
        URL детальной страницы товара.
        Используется для редиректов после создания/редактирования.
        """
        return reverse("catalog:product", kwargs={"pk": self.pk})

    @property
    def short_description(self) -> str:
        """
        Короткое описание для карточек на главной (до 100 символов).
        """
        text = (self.description or "").strip()
        return (text[:100] + "…") if len(text) > 100 else text
