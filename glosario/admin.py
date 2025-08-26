from django.contrib import admin

from . import models


class TerminoAdmin(admin.ModelAdmin):
    list_display = ["entrada", "descripcion"]
    list_filter = ['fuente']
    search_fields = ["entrada", "descripcion"]


admin.site.register(models.Termino, TerminoAdmin)


class FuenteAdmin(admin.ModelAdmin):
    list_display = ["alias", "descripcion"]


admin.site.register(models.Fuente, FuenteAdmin)
