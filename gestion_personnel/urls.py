from django.urls import path
from . import views

app_name = "gestion_personnel"

urlpatterns = [
    path('control-des-retards/<slug:slug>/', views.control_retard, name = 'control_retard'),
    #path('enregistrer-retard/<int:id>/', views.enregistrer_retards, name = 'retard'),
    path('retards/date/<slug:slug>/', views.liste_retards_par_date, name='liste_retards_par_date'),
    path('retards/graphe/<slug:slug>/', views.afficher_graphe_retards, name='graphe_retards'),
    path('retards/graphe-json/<slug:slug>/', views.donnees_retards_par_mois, name='donnees_retards_par_mois'),
]