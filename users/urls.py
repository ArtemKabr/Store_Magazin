"""URL-маршруты приложения users."""
from django.urls import path
from .views import (
    register_view,
    UserLoginView,
    logout_view,          # ✅ только функция logout_view
    profile_view,
    profile_edit_view,
)
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    # Регистрация / Авторизация
    path("register/", register_view, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),   # ✅ функция, а не класс

    # Профиль
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),

    # Восстановление пароля (пока можно без шаблонов)
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
