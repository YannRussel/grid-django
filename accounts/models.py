from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password

class ControleurManager(UserManager):
    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Crée un superuser avec un numéro de téléphone et un mot de passe.
        """
        if not phone_number:
            raise ValueError('Le numéro de téléphone doit être spécifié.')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Controleur(AbstractUser): 
    username = None  # Désactiver le champ username
    phone_number = models.CharField(max_length=20, unique=True)  # Le champ phone_number

    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('controleur', 'Contrôleur'),
        ('sous_controleur', 'Sous-contrôleur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sous_controleur')

    sites_autorises = models.ManyToManyField('relotagrid.Site', blank=True, related_name='controleurs_autorises')

    USERNAME_FIELD = 'phone_number'  # Utiliser phone_number comme identifiant
    REQUIRED_FIELDS = ['email']  # L'email est requis pour la création du superuser

    objects = ControleurManager()  # Utiliser le custom manager
    def save(self, *args, **kwargs):
        # Vérifie si le mot de passe n'est pas encore haché
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)