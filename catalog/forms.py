"""Формы приложения catalog."""
from django import forms
from .models import Product

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