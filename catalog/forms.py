"""Формы приложения catalog."""
from django import forms

class ContactForm(forms.Form):
    """
    Простая форма обратной связи.
    Поля минимальны, пригодны для демо-обработки на стороне контроллера.
    """
    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Сообщение", widget=forms.Textarea, max_length=2000)
