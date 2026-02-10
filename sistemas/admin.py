from django.contrib import admin

from sistemas import models


class SistemaAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "nombre_sistema",
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
        'finalidad',
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


class PerfilAdmin(admin.ModelAdmin):
    list_display = ["id_perfil", "usuario", "cometido"]

admin.site.register(models.Perfil, PerfilAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["login", "nombre_completo", "organismo"]
    search_fields = [
        'login',
        'nombre',
        'apellidos',
        'email',
        ]

admin.site.register(models.Usuario, UsuarioAdmin)


class InterlocutorAdmin(admin.ModelAdmin):
    list_display = [
        "id_interlocutor",
        "usuario",
        "organismo",
        ]
    search_fields = [
        'usuario__login',
        'usuario__nombre',
        'usuario__apellidos',
        'usuario__email',
        'organismo__nombre_organismo',
        ]

admin.site.register(models.Interlocutor, InterlocutorAdmin)


class FamiliaAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "nombre_familia",
        ]
    search_fields = [
        'nombre_familia',
        ]

admin.site.register(models.Familia, FamiliaAdmin)


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
