# catalog/views.py
"""Контроллеры (views) для приложения catalog."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ContactForm  # используется на /contacts/
from .models import Product, ContactInfo  # добавили ContactInfo


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Главная: список товаров с пагинацией.
    Параметр страницы: ?page=<num>
    """
    qs = Product.objects.select_related("category").order_by("-created_at")

    # Размер страницы можно поменять при необходимости
    paginator = Paginator(qs, 8)

    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # (опционально) выводим последние 5 в консоль для проверки
    last_five = qs[:5]
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
            "products": page_obj,          # теперь это страница
            "page_obj": page_obj,          # стандартное имя под пагинацию
            "paginator": paginator,
            "is_paginated": page_obj.has_other_pages(),
        },
    )


def product_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Детальная страница товара.
    """
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    return render(
        request,
        "catalog/product_detail.html",
        {
            "title": product.title,
            "product": product,
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
