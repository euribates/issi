#!/usr/bin/env python3

from django.urls import path

from . import views
from . import converters  # noqa: F401
app_name = 'directorio'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('organismo/<org:organismo>/', views.detalle_organismo),
    tie('organismo/<org:organismo>/estudio/', views.estudio_organismo),
    ]
