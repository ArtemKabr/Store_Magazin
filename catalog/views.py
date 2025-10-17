"""Контроллеры (views) для приложения catalog."""
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, ProductForm
from .models import Product, ContactInfo
import logging

logger = logging.getLogger(__name__)


@login_required(login_url="users:login")  # ✅ только авторизованные
def product_create_view(request):
    """Создание товара через форму."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm()
    return render(request, "catalog/product_form.html", {"title": "Добавить товар", "form": form})


def home_view(request: HttpRequest) -> HttpResponse:
    """Главная страница с пагинацией."""
    qs = Product.objects.select_related("category").order_by("-created_at")
    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
    return render(
        request,
        "catalog/home.html",
        {
            "title": "Магазин — Главная",
            "products": page_obj,
            "page_obj": page_obj,
            "paginator": paginator,
            "is_paginated": page_obj.has_other_pages(),
        },
    )


def product_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Детальная страница товара."""
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    return render(request, "catalog/product_detail.html", {"title": product.title, "product": product})


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
        {"title": "Контакты", "form": form, "success": success, "contacts": contacts},
    )



@login_required(login_url="users:login")
def product_create_view(request):
    """Создание товара текущим пользователем."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user  # назначаем владельца
            product.save()                 # сохраняем в базу
            return redirect(product.get_absolute_url())  # редирект на страницу товара
    else:
        form = ProductForm()
    return render(request, "catalog/product_form.html", {"form": form})


@login_required(login_url="users:login")  #  редактировать только авторизованным
def product_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование товара через форму."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "catalog/product_form.html",
        {"title": f"Редактировать: {product.title}", "form": form},
    )


@login_required(login_url="users:login")  #  удалять только авторизованным
def product_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление товара с подтверждением (только владелец или модератор)."""
    product = get_object_or_404(Product, pk=pk)

    # Проверка прав
    if request.user != product.owner and not request.user.has_perm("catalog.delete_product"):
        return HttpResponseForbidden("У вас нет прав на удаление этого товара.")

    if request.method == "POST":
        product.delete()
        return redirect("catalog:home")
    return render(
        request,
        "catalog/product_delete_confirm.html",
        {"title": f"Удалить: {product.title}", "product": product},
    )