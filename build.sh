#!/usr/bin/env bash
# Hata olursa işlemi durdur
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

if [ "$DJANGOSUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --no-input \
        --username "$DJANGOSUPERUSER_USERNAME" \
        --email "$DJANGOSUPERUSER_EMAIL" \
        --role admin \
        --phone "0500000000" \
        --expertise "Yazilim"
fi