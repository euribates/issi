from django.contrib import admin

from import_export.admin import ImportExportMixin

from juriscan import models

class JuriscanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        "pk",
        "titulo",
        "necesita_actualizar",
        ]
    search_fields = [
        'titulo',
        ]

admin.site.register(models.Juriscan, JuriscanAdmin)
