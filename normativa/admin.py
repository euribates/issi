from django.contrib import admin

from . import models


class RangoAdmin(admin.ModelAdmin):
    list_display = [
        "id_rango",
        "nombre_rango",
        "peso",
        ]


class NormaAdmin(admin.ModelAdmin):
    list_display = [
        "id_norma",
        "nombre_norma",
        "sobrenombre",
        "rango",
        "id_juriscan",
        ]
    search_fields = [
        "nombre_norma",
        "sobrenombre",
        ]


admin.site.register(models.Rango, RangoAdmin)
admin.site.register(models.Norma, NormaAdmin)
