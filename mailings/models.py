"""Модели сервиса рассылок."""
from django.conf import settings
from django.db import models


class Client(models.Model):
    """
    Получатель рассылки.
    owner — владелец (пользователь), для ограничения доступа по ТЗ.
    """
    email = models.EmailField("Email", unique=True)
    full_name = models.CharField("ФИО", max_length=255)
    comment = models.TextField("Комментарий", blank=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clients")

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        permissions = [
            ("view_all_clients", "Может просматривать всех клиентов (менеджер)"),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"


class Message(models.Model):
    """Шаблон сообщения."""
    subject = models.CharField("Тема письма", max_length=255)
    body = models.TextField("Тело письма")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("view_all_messages", "Может просматривать все сообщения (менеджер)"),
        ]

    def __str__(self) -> str:
        return self.subject


class Mailing(models.Model):
    """Рассылка сообщений по клиентам."""
    STATUS_CHOICES = (
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    )

    start_at = models.DateTimeField("Дата/время первой отправки")
    finish_at = models.DateTimeField("Дата/время окончания отправки")
    status = models.CharField("Статус", max_length=16, choices=STATUS_CHOICES, default="Создана")
    message = models.ForeignKey(Message, on_delete=models.PROTECT, related_name="mailings", verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, related_name="mailings", verbose_name="Получатели")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mailings")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("view_all_mailings", "Может просматривать все рассылки (менеджер)"),
            ("stop_mailings", "Может останавливать чужие рассылки (менеджер)"),
        ]

    def __str__(self) -> str:
        return f"Рассылка #{self.pk} — {self.status}"


class Attempt(models.Model):
    """Попытка отправки по рассылке."""
    STATUS_CHOICES = (
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="attempts", verbose_name="Рассылка")
    attempted_at = models.DateTimeField("Дата/время попытки", auto_now_add=True)
    status = models.CharField("Статус", max_length=16, choices=STATUS_CHOICES)
    server_response = models.TextField("Ответ почтового сервера", blank=True, default="")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self) -> str:
        return f"{self.mailing_id} — {self.status} — {self.attempted_at:%Y-%m-%d %H:%M}"
