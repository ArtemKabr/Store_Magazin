from django.urls import path
from . import views

urlpatterns = [
    # Клиенты
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/create/", views.ClientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/edit/", views.ClientUpdateView.as_view(), name="client_edit"),
    path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(), name="client_delete"),

    # Сообщения
    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/edit/", views.MessageUpdateView.as_view(), name="message_edit"),
    path("messages/<int:pk>/delete/", views.MessageDeleteView.as_view(), name="message_delete"),

    # Рассылки
    path("", views.MailingListView.as_view(), name="mailing_list"),
    path("create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("<int:pk>/edit/", views.MailingUpdateView.as_view(), name="mailing_edit"),
    path("<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),
    path("<int:pk>/run/", views.RunMailingView.as_view(), name="mailing_run"),

    # Попытки
    path("attempts/", views.AttemptListView.as_view(), name="attempt_list"),
]
