#!/usr/bin/env python3

from django.urls import path, register_converter

from . import views
from . import converters

app_name = 'sistemas'


register_converter(converters.SistemaConverter, 'si')


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('alta/', views.alta_sistema),
    tie('sistema/<si:sistema>/', views.detalle_sistema),
    tie('usuario/', views.listado_usuarios),
    ]
