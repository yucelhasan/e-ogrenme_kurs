#!/usr/bin/env bash
# Hata olursa işlemi durdur
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py axes_reset

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --no-input \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" \
        --role admin \
        --expertise "Sistem Yoneticisi" || true
fi