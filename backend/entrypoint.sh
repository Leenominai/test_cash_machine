#!/bin/bash

# Выполнение миграций и сборки статики
poetry install
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
poetry run pytest

# Запуск Gunicorn
exec "$@"
