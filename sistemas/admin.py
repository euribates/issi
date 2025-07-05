from django.contrib import admin

from sistemas.models import Sistema
from sistemas.models import Tema


class SistemaAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre", "descripcion", "tema"]
    list_filter = ['tema']


admin.site.register(Sistema, SistemaAdmin)


class TemaAdmin(admin.ModelAdmin):
    list_display = ["id_tema", "nombre_tema", "transversal"]


admin.site.register(Tema, TemaAdmin)
