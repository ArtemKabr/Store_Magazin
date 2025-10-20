#  Базовый образ
FROM python:3.12-slim
#  Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100
#  Установка системных пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
#  Рабочая директория
WORKDIR /var/www/html
#  Установка зависимостей Python
COPY requirements.txt /var/www/html/
RUN pip install --upgrade pip && pip install -r requirements.txt
#  Копирование проекта
COPY . /var/www/html/
#  Сборка статики
RUN python manage.py collectstatic --noinput || true
#  Экспонирование порта
EXPOSE 8000
#  Команда запуска приложения
CMD ["gunicorn", "store_magazin.wsgi:application", "--bind", "0.0.0.0:8000"]
