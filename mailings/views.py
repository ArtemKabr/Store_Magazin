"""Контроллеры CRUD для рассылок/клиентов/сообщений + попытки + ручной запуск."""
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from .models import Client, Message, Mailing, Attempt
from .forms import ClientForm, MessageForm, MailingForm
from .services import send_mailing_now


# ======== Фильтрация по владельцу ========
class OwnerQuerySetMixin:
    """Подмешивает фильтр по owner, кроме менеджеров с правами просмотра всех."""
    model = None
    view_all_perm = ""

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if self.view_all_perm and user.has_perm(self.view_all_perm):
            return qs
        return qs.filter(owner=user)

    def form_valid(self, form):
        # Прописываем владельца при создании
        if not form.instance.pk:
            form.instance.owner = self.request.user
        return super().form_valid(form)


# ======== Клиенты ========
@method_decorator(cache_page(30), name="dispatch")
class ClientListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Client
    view_all_perm = "mailings.view_all_clients"
    paginate_by = 20


class ClientCreateView(LoginRequiredMixin, OwnerQuerySetMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailings:client_list")


class ClientUpdateView(LoginRequiredMixin, OwnerQuerySetMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailings:client_list")


class ClientDeleteView(LoginRequiredMixin, OwnerQuerySetMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("mailings:client_list")
    template_name = "mailings/confirm_delete.html"


# ======== Сообщения ========
@method_decorator(cache_page(30), name="dispatch")
class MessageListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Message
    view_all_perm = "mailings.view_all_messages"
    paginate_by = 20


class MessageCreateView(LoginRequiredMixin, OwnerQuerySetMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")


class MessageUpdateView(LoginRequiredMixin, OwnerQuerySetMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")


class MessageDeleteView(LoginRequiredMixin, OwnerQuerySetMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailings:message_list")
    template_name = "mailings/confirm_delete.html"


# ======== Рассылки ========
@method_decorator(cache_page(30), name="dispatch")
class MailingListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Mailing
    view_all_perm = "mailings.view_all_mailings"
    paginate_by = 20


class MailingDetailView(LoginRequiredMixin, OwnerQuerySetMixin, DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, OwnerQuerySetMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("mailings:mailing_detail", kwargs={"pk": self.object.pk})


class MailingUpdateView(LoginRequiredMixin, OwnerQuerySetMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("mailings:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(LoginRequiredMixin, OwnerQuerySetMixin, DeleteView):
    """Удаление рассылки с подтверждением."""
    model = Mailing
    success_url = reverse_lazy("mailings:mailing_list")
    template_name = "mailings/confirm_delete.html"

# ======== Попытки ========
class AttemptListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Список попыток. Даем доступ только авторизованным.
    Менеджеру — все попытки, обычному — только свои через фильтр по Mailing.owner.
    """
    model = Attempt
    permission_required = "auth.view_user"  # любой авторизованный пройдёт, менеджеру можно расширить
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related("mailing")
        user = self.request.user
        if user.has_perm("mailings.view_all_mailings"):
            return qs
        return qs.filter(mailing__owner=user)


# ======== Ручной запуск рассылки ========
class RunMailingView(LoginRequiredMixin, OwnerQuerySetMixin, View):
    """Ручной запуск рассылки."""
    model = Mailing
    view_all_perm = "mailings.view_all_mailings"

    def post(self, request, pk):
        """Отправка рассылки вручную с проверкой прав доступа."""
        # Получаем queryset вручную (так как View не имеет get_queryset)
        qs = Mailing.objects.all()
        user = request.user
        if not user.has_perm(self.view_all_perm):
            qs = qs.filter(owner=user)

        mailing = get_object_or_404(qs, pk=pk)

        ok, fail = send_mailing_now(mailing.pk)
        messages.info(request, f"Отправлено: {ok}, ошибок: {fail}")
        return redirect("mailings:mailing_detail", pk=pk)