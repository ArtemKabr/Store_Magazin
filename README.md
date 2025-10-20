# 🛒 Store_Magazin

Учебный интернет-магазин на **Django 5.1.11** и **Python 3.12**,  
реализованный в рамках курса *«Знакомство с Django»*.

Проект демонстрирует принципы построения веб-приложений с кешированием, бизнес-логикой,  
сервисным слоем, авторизацией и настройкой окружения через `.env`.

---

## ⚙️ Технологический стек

| Компонент | Назначение |
|------------|------------|
| **Python 3.12** | Язык программирования |

| **Django 5.1.11** | Веб-фреймворк |

| **PostgreSQL** | Основная база данных |

| **Redis + django-redis** | Кеш и хранение сессий |

| **Bootstrap 5** | Адаптивная вёрстка шаблонов |

| **python-dotenv** | Работа с `.env`-файлом |

| **psycopg2-binary** | Драйвер PostgreSQL |

| **dotenv / os.getenv** | Конфигурация окружения |


---

## 🚀 Реализовано в проекте

### 🌐 Основные страницы
- **Главная** (`/`) — список товаров с пагинацией (последние 12), лог последних 5 в консоль.  
- **Контакты** (`/contacts/`) — форма обратной связи с валидацией и картой (iframe из БД).  
- **Категории** (`/category/<slug>/`) — страница товаров выбранной категории с низкоуровневым кешем.  
- **Детальная страница товара** (`/product/<pk>/`) — кеширование страницы через `@cache_page`.  

### ⚙️ Бизнес-логика и кеширование
- Подключён **Redis** с управлением через `.env`  
  (`CACHE_ENABLED=True/False`, `REDIS_LOCATION=redis://127.0.0.1:6379/1`).  
- Настроен fallback — при отсутствии Redis используется `LocMemCache`.  
- Добавлена сервисная функция `get_products_by_category(slug)` в `catalog/services.py`.  
- Низкоуровневое кеширование списка товаров по категориям (`cache.set`, `cache.get`).  
- Кеширование страницы товара с помощью `@cache_page(60 * 15)`.  

### 👤 Пользователи и авторизация
- Пользовательская модель `users.User` (через `AUTH_USER_MODEL`).  
- Авторизация, регистрация, выход из аккаунта.  
- Исправлен редирект после логина — больше нет `/accounts/profile/` (теперь `/`).  

### 🧰 Админка
- Регистрация моделей `Category`, `Product`, `ContactInfo`.  
- Автогенерация slug из названия.  
- Добавлено поле карты (iframe) в `ContactInfo`.

### 🛠 Кастомная команда
- `python manage.py seed_products` — очищает таблицы и добавляет тестовые категории и товары.

### 🧱 Шаблоны
- `base.html` — общий макет с Bootstrap 5.  
- `home.html` — главная страница.  
- `contacts.html` — форма обратной связи и карта.  
- `category_products.html` — страница категории с товарами.  
- `product_detail.html` — страница товара.


### ✉️ Сервис управления рассылками

Gолноценный модуль рассылок с веб-интерфейсом, CLI-командами
и разделением ролей пользователей.

## ⚙️ Возможности

Управление клиентами (Client) — имя, email, комментарий.

Создание сообщений (Message) — тема и тело письма.

Планирование рассылок (Mailing) — время начала, завершения, периодичность, статус.

Логирование попыток (Attempt) — результат и ответ сервера.

Ручной запуск рассылки через веб или консоль.

Статистика (всего, активных, уникальных получателей).

Отображение статистики только менеджерам и администраторам.


### 👥 Роли и права доступа
| Роль                              | Возможности                                      |
| --------------------------------- | ------------------------------------------------ |
| **Администратор**                 | Полный доступ ко всем рассылкам и пользователям. |
| **Менеджер (группа “Менеджеры”)** | Просмотр всех рассылок, запуск и анализ.         |
| **Пользователь**                  | Управление только своими рассылками и клиентами. |

Создание группы:
python manage.py create_managers_group


### 🧠 Внутренняя структура

| Компонент                       | Назначение                                                                 |
| ------------------------------- | -------------------------------------------------------------------------- |
| `mailings/models.py`            | Модели Client, Message, Mailing, Attempt.                                  |
| `mailings/views.py`             | CRUD через CBV (ListView, DetailView, CreateView, UpdateView, DeleteView). |
| `mailings/services.py`          | Отправка писем, логирование, обновление статуса.                           |
| `mailings/management/commands/` | Команды `send_mailing` и `create_managers_group`.                          |
| `mailings/templates/mailings/`  | Все шаблоны CRUD для рассылок и клиентов.                                  |


## При подключении SMTP через .env письма отправляются реально:

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=app-password


### 📊 Статистика рассылок

На главной странице (/) для менеджеров и администраторов отображается:

Всего рассылок

Активных

Уникальных получателей

Данные кешируются на 30 секунд.

## 📁 Основные шаблоны рассылок
attempt_list.html
client_form.html
client_list.html
confirm_delete.html
mailing_detail.html
mailing_form.html
mailing_list.html
message_form.html
message_list.html




## ⚙️ Настройки окружения

Файл `.env_template`:
```env
# 🔐 Безопасность
SECRET_KEY=dev-secret-key
DEBUG=True

# 🗄️ PostgreSQL
NAME=store_db
USER=postgres
PASSWORD=postgres
HOST=localhost
PORT=5432

## ⚙️ Кеширование
CACHE_ENABLED=True
REDIS_LOCATION=redis://127.0.0.1:6379/1



## 💡 Можно временно отключить кеширование:
CACHE_ENABLED=False

Установка и запуск (Windows)
# Клонировать проект
git clone https://github.com/ArtemKabr/Store_Magazin.git
cd Store_Magazin

# Создать виртуальное окружение
py -3.12 -m venv .venv
. .venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя (по желанию)
python manage.py createsuperuser

# Загрузить тестовые данные
python manage.py seed_products

# Запустить Redis (если включён кеш)
redis-server

# Запустить сервер Django
python manage.py runserver


🌍 Полезные URL
| Раздел         | URL                                                                                    
| -------------- | -------------------------------------------------------------------------------------- 
| 🏠 Главная     | http://127.0.0.1:8000/                                     
| 📞 Контакты    | http://127.0.0.1:8000/contacts/                   
| 🛒 Категории   | http://127.0.0.1:8000/category/smartfony/ 
| 📦 Товар       | http://127.0.0.1:8000/product/7/                
| ⚙️ Админка     | http://127.0.0.1:8000/admin/                       
| 👤 Вход        | http://127.0.0.1:8000/users/login/             
| 🔑 Регистрация | http://127.0.0.1:8000/users/register/       
| ✉️ Рассылки    | http://127.0.0.1:8000/mailings/                                              


            
### Проверка кеша в Redis

cd "C:\Program Files\Redis"
.\redis-cli.exe
SELECT 1
keys *

Если кеш включён, появятся ключи вроде:
store:views.decorators.cache.cache_page..GET.127.0.0.1.product.7
store:category_products_smartfony


Основные команды Django
| Задача                    | Команда                            |
| ------------------------- | ---------------------------------- |
| Создать миграции          | `python manage.py makemigrations`  |
| Применить миграции        | `python manage.py migrate`         |
| Сбросить БД               | `python manage.py flush`           |
| Создать суперпользователя | `python manage.py createsuperuser` |
| Загрузить тестовые данные | `python manage.py seed_products`   |
| Запустить сервер          | `python manage.py runserver`       |
| Запустить тесты           | `python manage.py test`            |



Особенности реализации

Кеш управляется переменной .env — легко включать/отключать.

При недоступном Redis используется безопасный LocMemCache.

CBV + миксины обеспечивают чистую архитектуру и разграничение доступа.

Отправка писем и логирование выведены в отдельный сервис.

Главная страница отображает динамическую статистику рассылок.

Полностью локализован на русский язык.

Код оформлен по PEP8 и best-practices Django.

---