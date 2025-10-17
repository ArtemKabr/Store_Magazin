from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import UserLoginForm, UserRegisterForm


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
        """Позволяет выполнять logout через ссылку или кнопку без CSRF."""
        return self.post(request, *args, **kwargs)

