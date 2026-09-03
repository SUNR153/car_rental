# Car Rental

Django-платформа для аренды автомобилей между пользователями: размещение объявлений, бронирование по датам, отзывы, избранное, уведомления и чат между владельцем и арендатором в реальном времени.

## Возможности

- Каталог автомобилей с фильтрами (категория, состояние, тип топлива, коробка передач)
- Бронирование с автоматическим расчётом стоимости по количеству дней
- Отзывы и рейтинги
- Избранное
- Уведомления
- Чат в реальном времени (Django Channels + Redis)
- Мультиязычность: English / Русский / Қазақша

## Стек

- **Backend:** Django, Django REST Framework, Django Channels
- **DB:** PostgreSQL
- **Realtime:** Redis (channels_redis)
- **Auth:** JWT (djangorestframework-simplejwt)
- **i18n:** django-modeltranslation

## Запуск локально

```bash
python -m venv myvenv
myvenv\Scripts\activate       # Windows
pip install -r req.txt

cp .env.example .env          # и заполнить своими значениями
python manage.py migrate
python manage.py seed_demo_data  # опционально: заполнить демо-данными (10 машин, 3 пользователя, отзывы)
python manage.py runserver
```

Тестовый вход после сидинга: `demo.customer1@vrooom.example` / `demopass123`

## Тесты

```bash
python manage.py test
```

## Переменные окружения

См. [.env.example](.env.example) — нужны `SECRET_KEY`, доступ к PostgreSQL и SMTP-данные для отправки почты (сброс пароля и т.п.).
