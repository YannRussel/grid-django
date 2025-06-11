from django.contrib import admin
from .models import Controleur
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html

# Register your models here.

from django.contrib.admin import AdminSite

admin.site.site_header = "Relota Grille de Controle"
admin.site.site_title = "grille de controle"
admin.site.index_title = "Bienvenue dans notre interface d'administration"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Controleur

@admin.register(Controleur)
class ControleurAdmin(UserAdmin):
    model = Controleur

    list_display = ('first_name', 'last_name', 'phone_number', 'role', 'is_active')
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('last_name',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'role', 'sites_autorises')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.site_url = reverse_lazy('relotagrid:acceuil')