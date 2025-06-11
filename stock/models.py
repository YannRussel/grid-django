from django.db import models
from relotagrid.models import Site

class Produit(models.Model):
    nom = models.CharField(max_length=255)
    conditionnement = models.CharField(max_length=255, blank=True)
    quantite_limite = models.PositiveIntegerField(help_text="Quantité minimale avant alerte")

    def __str__(self):
        return self.nom


class LivraisonMensuelle(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="livraisons_stock", null = True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="livraisons")
    mois = models.DateField(help_text="Ex: 2025-06-01 pour juin 2025")
    quantite_livree = models.PositiveIntegerField()

    class Meta:
        unique_together = ('site', 'produit', 'mois')
        ordering = ['-mois']

    def __str__(self):
        return f"{self.site.nom} - {self.produit.nom} ({self.mois.strftime('%B %Y')}) : {self.quantite_livree}"

class UtilisationJournal(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="utilisations")
    date_utilisation = models.DateField()
    quantite_utilisee = models.PositiveIntegerField()

    class Meta:
        ordering = ['-date_utilisation']

    def __str__(self):
        return f"{self.produit.nom} - {self.date_utilisation} : {self.quantite_utilisee}"
