"""Контроллеры (views) для приложения catalog."""

import logging

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from catalog.services import get_products_by_category

from .forms import ContactForm, ProductForm
from .models import ContactInfo, Product

logger = logging.getLogger(__name__)


# ==============================================================
# Главная страница с товарами + статистика рассылок
# ==============================================================
def home_view(request: HttpRequest) -> HttpResponse:
    """
    Главная страница магазина с пагинацией и статистикой рассылок.
    Данные рассылок кешируются на 30 секунд.
    """
    # --- товары ---
    qs = Product.objects.select_related("category").order_by("-created_at")
    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    # --- статистика рассылок ---
    cache_key = "home_stats_v1"
    data = cache.get(cache_key)

    if not data:
        try:
            from mailings.models import (  # импорт внутри, чтобы не ломалось при миграциях
                Client,
                Mailing,
            )

            total_mailings = Mailing.objects.count()
            active_mailings = Mailing.objects.filter(status="Запущена").count()
            unique_clients = Client.objects.count()
        except Exception:
            total_mailings = active_mailings = unique_clients = 0

        data = {
            "total_mailings": total_mailings,
            "active_mailings": active_mailings,
            "unique_clients": unique_clients,
        }
        cache.set(cache_key, data, 30)

    # --- флаг менеджера / админа ---
    is_manager = request.user.is_authenticated and (
        request.user.is_staff or request.user.groups.filter(name="Менеджеры").exists()
    )

    context = {
        "title": "Магазин — Главная",
        "products": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        **data,
        "is_manager": is_manager,  # 👈 теперь шаблон может просто проверить {% if is_manager %}
    }

    return render(request, "catalog/home.html", context)


# ==============================================================
# 🧩 Детальная страница товара (кеш Redis / LocMem)
# ==============================================================
@cache_page(60 * 15)
def product_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Детальная страница товара (кешируется на 15 минут)."""
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    return render(
        request,
        "catalog/product_detail.html",
        {"title": product.title, "product": product},
    )


# ==============================================================
#  CRUD: Создание / Редактирование / Удаление товара
# ==============================================================
@login_required(login_url="users:login")
def product_create_view(request):
    """Создание нового товара (только авторизованные пользователи)."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm()
    return render(
        request,
        "catalog/product_form.html",
        {"title": "Добавить товар", "form": form},
    )


@login_required(login_url="users:login")
def product_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование существующего товара."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "catalog/product_form.html",
        {"title": f"Редактировать: {product.title}", "form": form},
    )


@login_required(login_url="users:login")
def product_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление товара с подтверждением (только владелец или модератор)."""
    product = get_object_or_404(Product, pk=pk)

    # Проверка прав
    if request.user != getattr(product, "owner", None) and not request.user.has_perm("catalog.delete_product"):
        return HttpResponseForbidden("У вас нет прав на удаление этого товара.")

    if request.method == "POST":
        product.delete()
        return redirect("catalog:home")

    return render(
        request,
        "catalog/product_delete_confirm.html",
        {"title": f"Удалить: {product.title}", "product": product},
    )


# ==============================================================
# Категории и контакты
# ==============================================================
def category_products_view(request, slug: str):
    """
    Отображение всех товаров выбранной категории.
    Используется низкоуровневое кеширование.
    """
    cache_key = f"category_products_{slug}"
    products = cache.get(cache_key)

    if products is None:
        products = list(get_products_by_category(slug))
        cache.set(cache_key, products, 60 * 10)  # кеш 10 мин

    context = {
        "title": f"Товары категории: {slug}",
        "products": products,
    }
    return render(request, "catalog/category_products.html", context)


def contacts_view(request: HttpRequest) -> HttpResponse:
    """Контакты и форма обратной связи."""
    success = False
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        success = True
        form = ContactForm()
    contacts = ContactInfo.objects.first()
    return render(
        request,
        "catalog/contacts.html",
        {
            "title": "Контакты",
            "form": form,
            "success": success,
            "contacts": contacts,
        },
    )
