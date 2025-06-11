from django.contrib import admin
from .models import Produit, LivraisonMensuelle, UtilisationJournal


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'conditionnement', 'quantite_limite')
    search_fields = ('nom',)
    list_filter = ('conditionnement',)


@admin.register(LivraisonMensuelle)
class LivraisonMensuelleAdmin(admin.ModelAdmin):
    list_display = ('produit', 'mois', 'quantite_livree')
    list_filter = ('mois', 'produit')
    search_fields = ('produit__nom',)
    autocomplete_fields = ('produit',)


@admin.register(UtilisationJournal)
class UtilisationJournalAdmin(admin.ModelAdmin):
    list_display = ('produit', 'date_utilisation', 'quantite_utilisee')
    list_filter = ('date_utilisation', 'produit')
    search_fields = ('produit__nom',)
    autocomplete_fields = ('produit',)
