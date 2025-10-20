"""Формы для приложения users."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    """Форма авторизации пользователя (вход по email и паролю)."""

    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )


class UserRegisterForm(forms.ModelForm):
    """Регистрация нового пользователя."""

    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = User
        fields = ("email", "avatar", "phone", "country")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ваш email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Номер телефона"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Страна"}),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        """Проверка совпадения паролей."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "Пароли не совпадают.")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    """Обновление профиля (без смены пароля)."""

    class Meta:
        model = User
        fields = ("avatar", "phone", "country")
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }
