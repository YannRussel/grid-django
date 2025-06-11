from django.urls import path
from . import views

app_name = "relotagrid"

urlpatterns = [
    path('acceuil/', views.acceuil, name = 'acceuil'),
    path('site/<slug:slug>/',views.detail_site, name = 'detail_site'),
    path('vue-app/<slug:slug>/', views.vue_app, name = 'app_site'),
    path('liste-des-agents/', views.liste_agent, name = 'agents'),
    path('detail-agent/<int:id>/', views.agent_detail, name = 'detail_agent'),
    path('export-docx/', views.export_agents_docx, name='export_agents_docx'), # chemin pour une creation d'une liste des agents
    path('controller-un-site/<slug:slug>/', views.creer_grille, name = 'creation_grille'),
    path('controller-locale/<int:id>/', views.controller, name = 'controller_local'),
    #path('ajax/agents/<slug:slug>/', views.ajax_agents, name='ajax_agents'),
    path('enregistrer-grille/<int:local_id>/', views.enregistrer_grille, name = 'enregistrer_grille'),
    path('voir-tes-controles/<int:id>/', views.voir_controle, name = 'voir_controle'),
    path('grille-de-controle/<int:id>/', views.voir_grille, name = 'voir_grille'),
     path('graphique/performance/<slug:slug>/', views.performance_mensuelle_site, name='performance_mensuelle_site'),

]