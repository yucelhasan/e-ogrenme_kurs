#!/usr/bin/env bash
# Hata olursa işlemi durdur
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py axes_reset

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Admin kullanıcısı kontrol ediliyor ve oluşturuluyor..."
    cat <<EOF | python manage.py shell
from lms_app.models.users import CustomUser
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and not CustomUser.objects.filter(username=username).exists():
    CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='admin',
        phone='0500000000',
        expertise='Sistem Yoneticisi'
    )
    print(f"Superuser '{username}' basariyla olusturuldu.")
else:
    print(f"Superuser '{username}' zaten mevcut, atlandi.")
EOF
fi