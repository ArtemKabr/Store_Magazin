"""Контроллеры пользователей: регистрация, авторизация, профиль."""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm


def register_view(request):
    """
    Регистрация нового пользователя.
    После успешной регистрации — автоматический вход и приветственное письмо.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Автоматический вход
            login(request, user)

            # Отправка приветственного письма
            send_mail(
                "Добро пожаловать в FutureLab Store!",
                "Спасибо за регистрацию на нашем сайте 🎉",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )

            messages.success(request, "Регистрация прошла успешно!")
            return redirect("catalog:home")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


class UserLoginView(LoginView):
    """Авторизация пользователя."""
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("catalog:home")


class UserLogoutView(LogoutView):
    """Выход из аккаунта (по GET)."""
    next_page = reverse_lazy("catalog:home")

    def get(self, request, *args, **kwargs):
        """Позволяет выполнять logout через ссылку без CSRF."""
        return self.post(request, *args, **kwargs)


@login_required
def profile_view(request):
    """Просмотр профиля текущего пользователя."""
    return render(request, "users/profile.html")


@login_required
def profile_edit_view(request):
    """Редактирование профиля текущего пользователя."""
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён ✅")
            return redirect("users:profile")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "users/profile_edit.html", {"form": form})
