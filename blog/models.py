# blog/models.py
"""Модели блога."""
from django.db import models
from django.urls import reverse


class Post(models.Model):
    """
    Модель блоговой записи.
    Поля:
    - title: заголовок
    - content: текст статьи
    - preview: превью-изображение
    - created_at: дата создания
    - is_published: флаг публикации
    - views: счётчик просмотров
    """
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Содержимое", blank=True, default="")
    preview = models.ImageField("Превью", upload_to="blog/", blank=True, null=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=False)
    views = models.PositiveIntegerField("Просмотры", default=0, editable=False)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        """Строковое представление — заголовок статьи."""
        return self.title

    def get_absolute_url(self) -> str:
        """URL детальной страницы статьи."""
        return reverse("blog:post_detail", kwargs={"pk": self.pk})

