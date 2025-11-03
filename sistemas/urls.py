#!/usr/bin/env python3

from django.urls import path, register_converter

from . import views
from . import converters

app_name = 'sistemas'


register_converter(converters.SistemaConverter, 'si')
register_converter(converters.UserNameConverter, 'login')
register_converter(converters.OrganismoConverter, 'org')
register_converter(converters.EnteConverter, 'ent')
register_converter(converters.TemaConverter, 'tema')


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('alta/', views.alta_sistema),
    tie('sistema/<si:sistema>/', views.detalle_sistema),
    tie('sistema/<si:sistema>/editar/tema/', views.asignar_tema),
    tie('sistema/<si:sistema>/editar/proposito/', views.editar_proposito),
    tie('sistema/<si:sistema>/editar/organismo/', views.asignar_organismo),
    tie('entes/', views.listado_entes),
    tie('entes/<ent:ente>/', views.detalle_ente),
    tie('organismo/', views.listado_organismos),
    tie('organismo/<org:organismo>/', views.detalle_organismo),
    tie('usuario/', views.listado_usuarios),
    tie('usuario/buscar/', views.buscar_usuarios),
    tie('usuario/<login:usuario>/', views.detalle_usuario),
    tie('temas/', views.listado_temas),
    tie('temas/<tema:tema>/', views.detalle_tema),
    tie("patch/organismos/", views.patch_organismos),
    ]
