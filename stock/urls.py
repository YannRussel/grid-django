from django.urls import path
from . import views

app_name = 'gestion_stock'

urlpatterns = [
    path('site/<slug:slug_site>/livraisons/', views.livraisons_par_site, name='livraisons_par_site'),
    path('utilisation/<slug:slug>/', views.enregistrer_utilisation, name='enregistrer_utilisation'),
    path('creation-des-produits/', views.produit_create, name='enregistrer_produit'),
    path('produit/supprimer/<int:pk>/', views.produit_delete, name='supprimer_produit'),
    #Urls pour les livraisons
    path('site/<slug:slug>/livraisons-gestion/', views.enregistrer_livraison, name='enregistrer_livraison'),
    path('livraison/supprimer/<int:livraison_id>/', views.supprimer_livraison, name='supprimer_livraison'),


]