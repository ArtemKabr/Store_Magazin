import pytest
from django.contrib.auth import get_user_model

from mailings.models import Client, Mailing, Message

User = get_user_model()


@pytest.mark.django_db
def test_mailing_str_and_relations():
    """Проверка строкового представления рассылки и связей."""
    user = User.objects.create_user(email="demo@example.com", password="12345")
    msg = Message.objects.create(subject="Тест", body="Привет!")
    client = Client.objects.create(full_name="Артём", email="a@test.ru")

    mailing = Mailing.objects.create(
        message=msg,
        owner_id=user.id,
        start_at="2025-10-17T10:00:00Z",
        finish_at="2025-10-18T10:00:00Z",
    )

    mailing.clients.add(client)
    assert str(mailing) == "Тест"
    assert mailing.clients.count() == 1
