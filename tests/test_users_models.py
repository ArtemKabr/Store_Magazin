import pytest

from users.models import User


@pytest.mark.django_db
def test_create_user_with_email():
    """Проверяет создание пользователя с email."""
    user = User.objects.create_user(email="test@example.com", password="12345", country="RU")
    assert user.email == "test@example.com"
    assert user.check_password("12345") is True


@pytest.mark.django_db
def test_user_str_method():
    """Проверяет строковое представление модели пользователя."""
    user = User.objects.create(email="demo@example.com")
    assert str(user) == "demo@example.com"
