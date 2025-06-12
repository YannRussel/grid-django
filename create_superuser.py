import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grid.settings")  # remplace par ton module settings
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Valeurs à personnaliser ou à lier à des variables d'environnement
phone_number = os.environ.get("DJANGO_SUPERUSER_PHONE", "065215758")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "yann.russel.webwriter@gmail.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "LinuxCode@123")

if not User.objects.filter(phone_number=phone_number).exists():
    User.objects.create_superuser(
        phone_number=phone_number,
        email=email,
        password=password,
        role='admin'  # Assure que le rôle correspond
    )
    print("Superutilisateur créé avec succès.")
else:
    print("Superutilisateur déjà existant.")
