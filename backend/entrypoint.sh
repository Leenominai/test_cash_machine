#!/bin/bash

# Выполнение миграций и сборки статики
poetry install
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser \
  --username admin \
  --email admin@yandex.ru \
  --password test_admin \
  --confirm_password test_admin

# Запуск Gunicorn
exec "$@"
