#!/usr/bin/env bash

# Arrêter le script dès qu'une commande échoue
set -o errexit

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques pour Whitenoise
python manage.py collectstatic --no-input

# Appliquer les migrations
python manage.py migrate

# Créer un superuser si nécessaire
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
