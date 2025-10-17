"""URL-маршруты приложения users."""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register_view,
    UserLoginView,
    UserLogoutView,
    profile_view,
    profile_edit_view,
)

app_name = "users"

urlpatterns = [
    # Регистрация / Авторизация
    path("register/", register_view, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),

    # 👤 Профиль
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),

    # 🔁 Восстановление пароля (пока можно без шаблонов)
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
