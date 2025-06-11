from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name  = 'accounts'
urlpatterns = [
     path('', views.index, name = 'index'),
     path('connexion-user/', views.login_user, name ='connexion'),
     path('deconnexion/', views.logout_user, name = 'deconnexion'),

     #Configuration du mot de passe oublié ...
     path('motdepasse-oublie/', views.motdepasse_oublie, name='motdepasse_oublie'),
     path('reset/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]
