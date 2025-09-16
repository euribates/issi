from django.contrib import admin

from directorio import models


class OrganismoAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "dir3",
        "id_sirhus",
        "nombre_organismo",
        "categoria",
        ]
    list_filter = [
        'categoria',
        ]
    search_fields = [
        'nombre_organismo',
        'dir3',
        'categoria',
        ]

admin.site.register(models.Organismo, OrganismoAdmin)


class EnteAdmin(admin.ModelAdmin):
    list_display = [
        "id_ente",
        "organismo__nombre_organismo",
        ]
    search_fields = [
        'id_ente',
        'organismo__nombre_organismo',
        ]

admin.site.register(models.Ente, EnteAdmin)



