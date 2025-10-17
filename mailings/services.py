"""Сервисные функции рассылок."""
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Mailing, Attempt


def send_mailing_now(mailing_id: int) -> tuple[int, int]:
    """
    Отправляет письма по рассылке вручную.
    Возвращает (успешно, неуспешно).
    """
    mailing = Mailing.objects.select_related("message").prefetch_related("clients").get(pk=mailing_id)

    ok, fail = 0, 0
    for client in mailing.clients.all():
        try:
            sent = send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            Attempt.objects.create(
                mailing=mailing,
                status="Успешно" if sent else "Не успешно",
                server_response="OK" if sent else "send_mail() вернул 0",
            )
            ok += 1 if sent else 0
            fail += 0 if sent else 1
        except Exception as e:
            Attempt.objects.create(
                mailing=mailing, status="Не успешно", server_response=str(e)
            )
            fail += 1

    # Обновим статус по времени
    now = timezone.now()
    if mailing.start_at <= now <= mailing.finish_at:
        mailing.status = "Запущена"
    elif now > mailing.finish_at:
        mailing.status = "Завершена"
    mailing.save(update_fields=["status"])
    return ok, fail
