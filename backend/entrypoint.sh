#!/bin/bash

# Выполнение миграций и сборки статики
poetry install
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

# Запуск Gunicorn
exec "$@"
