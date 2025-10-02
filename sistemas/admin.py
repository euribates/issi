from django.contrib import admin

from sistemas import models


class SistemaAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "nombre",
        "descripcion",
        "tema",
        "es_transversal",
        ]
    list_filter = ['tema', "es_transversal"]
    exclude = [
        'icono_width',
        'icono_height',
        ]
    search_fields = [
        'codigo',
        'descripcion',
        'proposito',
        ]

admin.site.register(models.Sistema, SistemaAdmin)


class ActivoAdmin(admin.ModelAdmin):
    list_display = [
        "id_activo",
        "nombre_activo",
        "es_prioritario",
        "esta_georeferenciado",
        "datos_personales",
        ]
    list_filter = [
        "es_prioritario",
        "esta_georeferenciado",
        "datos_personales",
        ]

admin.site.register(models.Activo, ActivoAdmin)


class TemaAdmin(admin.ModelAdmin):
    list_display = ["id_tema", "nombre_tema", "transversal"]

admin.site.register(models.Tema, TemaAdmin)


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["login", "nombre_completo", "organismo"]

admin.site.register(models.Usuario, UsuarioAdmin)
