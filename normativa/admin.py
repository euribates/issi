from django.contrib import admin

from .models import Norma


class NormaAdmin(admin.ModelAdmin):
    list_display = [
        "id_norma",
        "nombre_norma",
        "sobrenombre",
        "id_juriscan",
        ]
    search_fields = [
        "nombre_norma",
        "sobrenombre",
        ]


admin.site.register(Norma, NormaAdmin)
