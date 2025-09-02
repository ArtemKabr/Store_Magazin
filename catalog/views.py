"""Контроллеры (views) для приложения catalog."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import ContactForm  # используется на /contacts/

def home_view(request: HttpRequest) -> HttpResponse:
    """
    Домашняя страница магазина.
    Рендерит шаблон 'catalog/home.html' через функцию render.
    """
    context = {"title": "Магазин — Главная"}
    return render(request, "catalog/home.html", context)


def contacts_view(request: HttpRequest) -> HttpResponse:
    """
    Страница контактов.
    Обрабатывает форму обратной связи: при успешной валидации показывает сообщение.
    """
    success = False
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # Здесь может быть логика сохранения в БД/отправки email.
        # Для учебной задачи отметим успешную отправку и очистим форму.
        success = True
        form = ContactForm()

    context = {
        "title": "Контакты",
        "form": form,
        "success": success,
    }
    return render(request, "catalog/contacts.html", context)
from django.shortcuts import render

# Create your views here.
