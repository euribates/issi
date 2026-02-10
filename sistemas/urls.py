#!/usr/bin/env python3

from django.urls import path

from . import views
from . import converters  # noqa: F401

app_name = 'sistemas'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('alta/', views.alta_sistema),
    tie('sistema/<si:sistema>/', views.detalle_sistema),
    tie('sistema/<si:sistema>/editar/', views.editar_sistema),
    tie('sistema/<si:sistema>/editar/tema/', views.asignar_tema),
    tie('sistema/<si:sistema>/editar/familia/', views.asignar_familia),
    tie('sistema/<si:sistema>/editar/finalidad/', views.editar_finalidad),
    tie('sistema/<si:sistema>/editar/descripcion/', views.editar_descripcion),
    tie('sistema/<si:sistema>/editar/organismo/', views.asignar_organismo),
    tie('sistema/<si:sistema>/asignar/responsable/', views.asignar_responsable),
    tie('sistema/<si:sistema>/asignar/normativa/', views.asignar_normativa),
    tie('sistema/<si:sistema>/asignar/icono/', views.asignar_icono),
    tie('sistema/<si:sistema>/asignar/icono/', views.asignar_icono),
    tie('sistema/<si:sistema>/conmutar/<str:campo>/', views.conmutar_campo),
    tie('perfil/<int:id_perfil>/borrar/', views.borrar_perfil),
    tie('entes/', views.listado_entes),
    tie('entes/<ent:ente>/', views.detalle_ente),
    tie('entes/<ent:ente>/asignar/interlocutor/', views.asignar_interlocutor),
    tie('organismo/', views.listado_organismos),
    tie('organismo/<org:organismo>/', views.detalle_organismo),
    tie('usuario/', views.listado_usuarios),
    tie('usuario/buscar/', views.buscar_usuarios),
    tie('usuario/alta/', views.alta_usuario),
    tie('usuario/<usr:usuario>/', views.detalle_usuario),
    tie('temas/', views.listado_temas),
    tie('temas/<tema:tema>/', views.detalle_tema),
    tie('familias/', views.listado_familias),
    tie('familias/<fam:familia>/', views.detalle_familia),
    tie('activos/', views.listado_activos),
    tie('pendientes/', views.pendientes),
    tie('pendientes/temas/', views.sistemas_sin_tema),
    tie('exportar/', views.exportar_sistemas),
    tie('exportar/<ent:ente>/', views.exportar_sistemas_por_ente),
    tie('exportar/todos/', views.exportar_sistemas_todos),
    tie('importar/', views.importar_sistemas),
    tie("patch/organismos/", views.patch_organismos),
    tie("patch/usuarios/", views.patch_usuarios),
    tie("patch/sistemas/", views.patch_sistemas),
    ]
