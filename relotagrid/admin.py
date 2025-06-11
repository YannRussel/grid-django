from django.contrib import admin
from .models import Site, LocalType, ElementControl, Agent, Critere, Local, GrilleControl, ControlGrille


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'description')
    search_fields = ('nom',)
    prepopulated_fields = {'slug': ('nom',)}
    fieldsets = (
        ("Informations sur le site", {
            'fields': ('nom', 'slug', 'description')
        }),
    )


@admin.register(LocalType)
class LocalTypeAdmin(admin.ModelAdmin):
    list_display = ('nom_local',)
    search_fields = ('nom_local',)


@admin.register(ElementControl)
class ElementControlAdmin(admin.ModelAdmin):
    list_display = ('libelle',)
    search_fields = ('libelle',)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'adresse', 'date_naissance', 'lieu_naissance')
    search_fields = ('nom', 'prenom', 'adresse', 'lieu_naissance')
    fieldsets = (
        ("Identité", {
            'fields': ('nom', 'prenom', 'telephone', 'adresse', 'date_naissance', 'lieu_naissance')
        }),
        ("Documents", {
            'fields': ('image', 'cv')
        }),
        ("Sites", {
            'fields': ('site',)
        }),
    )
    filter_horizontal = ('site',)



@admin.register(Critere)
class CritereAdmin(admin.ModelAdmin):
    list_display = ('critere',)
    search_fields = ('critere',)


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('site', 'local_type')
    list_filter = ('site', 'local_type')
    filter_horizontal = ('element_controle',)

admin.site.register(GrilleControl)
admin.site.register(ControlGrille)