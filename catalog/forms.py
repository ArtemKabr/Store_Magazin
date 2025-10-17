# catalog/forms.py
"""Формы приложения catalog."""
from typing import Iterable

from django import forms
from django.core.exceptions import ValidationError

from .models import Product

# Запрещённые слова
FORBIDDEN_WORDS: tuple[str, ...] = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)


def _check_forbidden(value: str, words: Iterable[str]) -> None:
    """Проверяет текст на запрещённые слова (без учёта регистра)."""
    low = (value or "").lower()
    for w in words:
        if w in low:
            raise ValidationError(f"Запрещённое слово: «{w}». Уберите его из текста.")


class ContactForm(forms.Form):
    """
    Простая форма обратной связи.
    Поля минимальны, пригодны для демо-обработки на стороне контроллера.
    """

    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Сообщение", widget=forms.Textarea, max_length=2000)


class ProductForm(forms.ModelForm):
    """
    Форма добавления/редактирования товара.
    """

    class Meta:
        model = Product
        fields = ("title", "slug", "category", "image", "description", "price", "is_published")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        """Стилизация Bootstrap + чекбокс."""
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "is_published":
                field.widget = forms.CheckboxInput(attrs={"class": "form-check-input"})
            else:
                css = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{css} form-control".strip()

    def clean_title(self) -> str:
        """Запрещённые слова в названии."""
        value: str = self.cleaned_data.get("title", "")
        _check_forbidden(value, FORBIDDEN_WORDS)
        return value

    def clean_description(self) -> str:
        """Запрещённые слова в описании."""
        value: str = self.cleaned_data.get("description", "")
        _check_forbidden(value, FORBIDDEN_WORDS)
        return value

    def clean_price(self):
        """Цена не может быть отрицательной."""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        """
        Проверка изображения:
        - допустимы только JPEG/PNG
        - размер не более 5 МБ
        """
        image = self.cleaned_data.get("image")
        if not image:
            return image

        content_type = getattr(image, "content_type", "")
        if content_type not in ("image/jpeg", "image/png"):
            raise ValidationError("Допустимы только изображения JPEG или PNG.")

        if image.size > 5 * 1024 * 1024:
            raise ValidationError("Размер файла не должен превышать 5 МБ.")

        return image
