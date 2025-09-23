# catalog/views.py
"""Контроллеры (views) для приложения catalog на CBV."""
from blog.models import Post
from typing import Any, Dict

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView
from django.db.models import F

from .forms import ContactForm, ProductForm
from .models import Product, ContactInfo


class HomeView(ListView):
    """
    Главная страница: список товаров с пагинацией.
    Параметр страницы: ?page=<num>
    """
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        """Оптимизированный ORM-запрос + сортировка по дате создания (убыв.)."""
        return Product.objects.select_related("category").order_by("-created_at")

    def get_context_data(self, **kwargs):
        """
        Расширяем контекст: последние 3 опубликованные статьи блога.
        """
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Магазин — Главная"
        ctx["latest_posts"] = Post.objects.filter(is_published=True).order_by("-created_at")[:3]
        return ctx


class ProductDetailView(DetailView):
    """
    Детальная страница товара.
    """
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        """Жадно подтягиваем категорию."""
        return Product.objects.select_related("category")


class ProductCreateView(CreateView):
    """
    Создание товара через форму.
    После успешного сохранения — редирект на детальную страницу товара
    (за счёт model.get_absolute_url()).
    """
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    # success_url не нужен, т.к. у модели должен быть get_absolute_url()


class ContactsView(FormView):
    """
    Контакты с формой обратной связи.
    После успешной отправки показываем одноразовый флаг success.
    """
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")

    def form_valid(self, form: ContactForm) -> HttpResponse:
        """
        Здесь можно добавить сохранение/отправку email.
        Для демо — считаем, что письмо отправлено.
        """
        # TODO: логика отправки письма/сохранения в БД
        self.request.session["contacts_success"] = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Пробрасываем ContactInfo и одноразовый success-флаг в шаблон."""
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Контакты"
        ctx["contacts"] = ContactInfo.objects.first()
        ctx["success"] = self.request.session.pop("contacts_success", False)
        return ctx
