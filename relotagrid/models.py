from django.db import models
from django.utils.text import slugify
from .validators import validate_numero_congo
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.

class Site(models.Model) :
    nom = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "1. Creer un site"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nom)
            slug = base_slug
            counter = 1
            while Site.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
    

class LocalType(models.Model) :
    nom_local = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "2. Creer des types de locaux"
    
    def __str__(self):
        return self.nom_local
    
class Critere(models.Model) :
    critere = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "3. Creer des criteres"

    def __str__(self):
        return self.critere
    

class ElementControl(models.Model) :
    libelle = models.CharField(max_length=100)
    critere = models.ManyToManyField(Critere)

    class Meta:
        verbose_name_plural = "4. Creer des elements de controle"

    def __str__(self):
        return self.libelle

from django.db import models

class Agent(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='agents/images/', blank=True, null=True)
    cv = models.FileField(upload_to='agents/cv/', blank=True, null=True)
    site = models.ManyToManyField('Site', related_name='agents')

    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    
class Local(models.Model) :
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    local_type = models.ForeignKey(LocalType, on_delete=models.CASCADE)
    element_controle = models.ManyToManyField(ElementControl)

    class Meta:
        verbose_name_plural = "6. Creation des Locals"

class GrilleControl(models.Model) :
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def total_points(self):
        return sum(note.note for note in self.notes.all())

    def max_possible_points(self):
        return self.notes.count() * 3

    def appreciation(self):
        total = self.total_points()
        maximum = self.max_possible_points()

        if maximum == 0:
            return "Non évalué"

        pourcentage = (total / maximum) * 100

        if pourcentage >= 80:
            return "Excellent"
        elif pourcentage >= 50:
            return "Passable"
        else:
            return "Insuffisant"
    
    @property
    def agent(self):
        first_note = self.notes.first()
        return first_note.agent if first_note else None


class ControlGrille(models.Model):
    grille = models.ForeignKey(GrilleControl, on_delete=models.CASCADE, related_name='notes')
    element_controle = models.ForeignKey(ElementControl, on_delete=models.CASCADE)
    critere = models.ForeignKey(Critere, on_delete=models.CASCADE)
    note = models.IntegerField()
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.element_controle.libelle} - {self.critere.critere} : {self.note}"

