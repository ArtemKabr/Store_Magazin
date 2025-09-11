# catalog/views.py
"""Контроллеры (views) для приложения catalog."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import ContactForm  # используется на /contacts/
from .models import Product, ContactInfo  # добавили ContactInfo


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Главная: выводит список товаров и печатает в консоль последние 5.

    Вывод в консоль нужен для проверки ДЗ:
    пример строки — "[home] Последние 5: 12:iPhone 14 (799.99 ₽), ..."
    """
    # товары для страницы
    products = Product.objects.select_related("category").order_by("-created_at")[:12]

    # последние 5 для консоли
    last_five = Product.objects.order_by("-created_at")[:5]
    print(
        "[home] Последние 5:",
        ", ".join(f"{p.id}:{p.title} ({p.price} ₽)" for p in last_five),
        flush=True,
    )

    return render(
        request,
        "catalog/home.html",
        {
            "title": "Магазин — Главная",
            "products": products,
        },
    )


def contacts_view(request: HttpRequest) -> HttpResponse:
    success = False
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        success = True
        form = ContactForm()

    contacts = ContactInfo.objects.first()

    return render(request, "catalog/contacts.html", {
        "title": "Контакты",
        "form": form,
        "success": success,
        "contacts": contacts,
    })
