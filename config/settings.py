# config/settings.py
"""Основные настройки Django-проекта 'Store_Magazin' / 'Сервис управления рассылками'."""
from pathlib import Path
import environ

# ==========================================================
# Базовые пути и переменные окружения
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Инициализация django-environ
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "dev-secret-key"),
    ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
    CACHE_ENABLED=(bool, True),
    REDIS_LOCATION=(str, "redis://127.0.0.1:6379/1"),
    EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
    DEFAULT_FROM_EMAIL=(str, "noreply@example.com"),
)

# Загружаем .env из корня проекта
environ.Env.read_env(BASE_DIR / ".env")

# ==========================================================
#  Безопасность и отладка
# ==========================================================
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# ==========================================================
#  Установленные приложения
# ==========================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Основные приложения проекта
    "catalog",
    "users",
    "mailings",  # ✅ приложение рассылок
]

# ==========================================================
# ⚙ Middleware
# ==========================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ==========================================================
#  Шаблоны
# ==========================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ==========================================================
# 🗄 База данных (PostgreSQL из .env)
# ==========================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("NAME"),
        "USER": env("USER"),
        "PASSWORD": env("PASSWORD"),
        "HOST": env("HOST", default="localhost"),
        "PORT": env("PORT", default="5432"),
    }
}

# ==========================================================
#  Локализация
# ==========================================================
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# ==========================================================
# 🖼 Статика и медиа
# ==========================================================
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==========================================================
#  Пользовательская модель
# ==========================================================
AUTH_USER_MODEL = "users.User"

# ==========================================================
#  Аутентификация / редиректы
# ==========================================================
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "catalog:home"
LOGOUT_REDIRECT_URL = "catalog:home"

# ==========================================================
# Почта
# ==========================================================
EMAIL_BACKEND = env("EMAIL_BACKEND")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

# ==========================================================
#  Кеширование (Redis или LocMem)
# ==========================================================
CACHE_ENABLED = env("CACHE_ENABLED")
REDIS_LOCATION = env("REDIS_LOCATION")

if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_LOCATION,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "store",
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    # Фолбэк — in-memory кеш (для dev/тестов)
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.db"

# ==========================================================
#  Служебные настройки
# ==========================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
