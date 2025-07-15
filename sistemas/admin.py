from django.contrib import admin

from sistemas.models import Sistema
from sistemas.models import Tema


class SistemaAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre", "descripcion", "tema", "es_transversal"]
    list_filter = ['tema', "es_transversal"]


admin.site.register(Sistema, SistemaAdmin)


class TemaAdmin(admin.ModelAdmin):
    list_display = ["id_tema", "nombre_tema", "transversal"]


admin.site.register(Tema, TemaAdmin)
