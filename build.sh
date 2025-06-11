#!/usr/bin/env bash

# build.sh

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Crée un superuser avec numéro de téléphone s'il n'existe pas
echo "
from accounts.models import Controleur
if not Controleur.objects.filter(phone_number='${DJANGO_SU_PHONE}').exists():
    Controleur.objects.create_superuser(
        phone_number='${DJANGO_SU_PHONE}',
        email='${DJANGO_SU_EMAIL}',
        password='${DJANGO_SU_PASS}',
        role='admin'
    )
" | python manage.py shell
