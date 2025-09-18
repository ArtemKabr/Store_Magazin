# 🧰 Шпора по Django-командам (Windows, Python 3.12, UTF-8, проект Store_Magazin),

Все примеры ниже запускаются из корня проекта и **всегда** с флагом `-Xutf8`, чтобы не ловить кракозябры в кириллице.

---

## 🎯 Окружение

bash
# Создать и активировать виртуальное окружение
py -3.12 -m venv .venv
. .venv\Scripts\activate


# Установить зависимости
pip install -r requirements.txt


### ⚙️ Миграции (основа работы с БД)

Создать миграции по изменениям моделей
python -Xutf8 manage.py makemigrations

Создать ПУСТУЮ миграцию (ручные операции/RunPython/RunSQL)
python -Xutf8 manage.py makemigrations catalog --empty --name maintenance

 Применить миграции
python -Xutf8 manage.py migrate

Откатить миграции приложения catalog до нуля (полный rollback app-а)
python -Xutf8 manage.py migrate catalog zero

План миграций (что будет применено/откачено)
python -Xutf8 manage.py showmigrations catalog --plan

Посмотреть SQL для конкретной миграции
python -Xutf8 manage.py sqlmigrate catalog 0001

Проверить конфигурацию и проблемы
python -Xutf8 manage.py check
Для прод-советов по безопасности (даже в dev полезно)
python -Xutf8 manage.py check --deploy


### 🗃️ Работа с данными (фикстуры, дампы, загрузка)
 ВЫГРУЗИТЬ ВСЁ из приложения catalog (читаемо с отступами)
python -Xutf8 manage.py dumpdata catalog --indent 2 > catalog/fixtures/catalog.json

ВЫГРУЗИТЬ выборочно (Category + Product)
python -Xutf8 manage.py dumpdata catalog.Category catalog.Product --indent 2 > catalog/fixtures/products.json

ВЫГРУЗИТЬ ContactInfo (контакты + карта)
python -Xutf8 manage.py dumpdata catalog.ContactInfo --indent 2 > catalog/fixtures/contacts.json
 
Рекомендованный дамп БЕЗ служебных таблиц (чище для dev)
python -Xutf8 manage.py dumpdata \
  --indent 2 \
  --natural-foreign --natural-primary \
  --exclude auth.permission \
  --exclude contenttypes \
  > catalog/fixtures/clean_dump.json

ЗАГРУЗИТЬ фикстуру (ищется в <app>/fixtures автоматически)
python -Xutf8 manage.py loaddata products.json

Полная очистка данных (оставляет структуру таблиц)
python -Xutf8 manage.py flush

Сгенерировать SQL, который бы выполнил flush (без выполнения)
python -Xutf8 manage.py sqlflush


### 👤 Пользователи/админка
Создать суперпользователя
python -Xutf8 manage.py createsuperuser

Создать суперпользователя с указанием имени/почты (часть будет спрошена)
python -Xutf8 manage.py createsuperuser --username admin --email admin@example.com

Сменить пароль
python -Xutf8 manage.py changepassword admin


### 🛠 Кастомные команды проекта
Заполнить тестовыми данными (очищает Product/Category и создаёт заново)
python -Xutf8 manage.py seed_products

(опционально) с параметрами, если предусмотрены:
python -Xutf8 manage.py seed_products --count 30 --no-flush


### 🖥️ Запуск/отладка
Запустить dev-сервер на localhost:8000
python -Xutf8 manage.py runserver

Запустить на всех интерфейсах (для локальной сети)
python -Xutf8 manage.py runserver 0.0.0.0:8000

Увеличить подробность логов запуска
python -Xutf8 manage.py runserver --verbosity 3

Указать альтернативные настройки (если сделаешь config.settings_dev и т.п.)
python -Xutf8 manage.py runserver --settings=config.settings


### 🔎 Django shell (быстрые операции с БД)
Открыть интерактивный shell
python -Xutf8 manage.py shell

Примеры полезных сниппетов (копируй прямо в shell):
# 1) Быстрые проверки/создание данных
from catalog.models import Category, Product, ContactInfo
from decimal import Decimal

cat, _ = Category.objects.get_or_create(name="Тестовая", defaults={"slug":"test"})
p = Product.objects.create(title="Тестовый товар", slug="test-product", price=Decimal("123.45"), category=cat)

# 2) Последние 5 товаров (как в логе home_view)
list(Product.objects.order_by("-created_at").values_list("id","title","price")[:5])

# 3) Контакты (проверка наличия карты)
c = ContactInfo.objects.first(); (bool(c), (c and bool(c.map_embed)))


### Тесты (встроенный раннер Django)
Запустить все тесты
python -Xutf8 manage.py test -v 2

Запустить тесты только приложения catalog
python -Xutf8 manage.py test catalog -v 2

Запустить один файл/кейс (если появятся)
python -Xutf8 manage.py test catalog.tests.test_models -v 2


### 🗂️ Статика/медиа (на будущее)
Сбор статики (понадобится в проде; укажи STATIC_ROOT в settings.py)
python -Xutf8 manage.py collectstatic


### 🌐 Локализация (если добавишь переводы)
Сгенерировать .po-файлы для языка ru
python -Xutf8 manage.py makemessages -l ru

Скомпилировать переводы (.po -> .mo)
python -Xutf8 manage.py compilemessages


### 🏗️ Реверс-инжиниринг БД (если есть готовая БД, а моделей нет)
Сгенерировать модели из существующей БД (черновик)
python -Xutf8 manage.py inspectdb > catalog/models_from_db.py


### 🧭 Диагностика и конфиги
Посмотреть отличия текущих настроек от дефолтных
python -Xutf8 manage.py diffsettings

Вывести список миграций и их состояние
python -Xutf8 manage.py showmigrations


### 🌍 Полезные URL проекта (быстрые ссылки)

Админка: http://127.0.0.1:8000/admin/

Главная: http://127.0.0.1:8000/

Контакты: http://127.0.0.1:8000/contacts/


