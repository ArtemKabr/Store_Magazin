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
ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1", "b94628c9e1a56f.lhr.life", ".loca.lt"]
CSRF_TRUSTED_ORIGINS = ["https://*.loca.lt"]

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
# База данных (PostgreSQL из .env)
# ==========================================================
DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

# ==========================================================
# Локализация
# ==========================================================
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# ==========================================================
# Статика и медиа
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
# CACHE_ENABLED = env("CACHE_ENABLED")
# REDIS_LOCATION = env("REDIS_LOCATION")

# Читаем переменные окружения с безопасными значениями по умолчанию
CACHE_ENABLED = env.bool("CACHE_ENABLED", default=False)
REDIS_LOCATION = env("REDIS_LOCATION", default="redis://127.0.0.1:6379/1")

if CACHE_ENABLED:
    # Используем Redis как backend кеша
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

    # Хранение сессий в Redis
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

    # Для отладки удобно видеть, что кеш включен
    print("✅ Redis-кеш активен:", REDIS_LOCATION)

else:
    # Фолбэк — in-memory кеш (используется в dev/test окружении)
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-store-magazin",
        }
    }

    # Сессии будут храниться в БД
    SESSION_ENGINE = "django.contrib.sessions.backends.db"

    print("⚠️ Redis отключен — используется локальный кеш")

# ==========================================================
#  Служебные настройки
# ==========================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CSRF_TRUSTED_ORIGINS = ["https://*.lhr.life"]

