#!/usr/bin/env python3

from django.urls import path, register_converter

from . import views
from . import converters

app_name = 'directorio'

register_converter(converters.OrganismoConverter, 'org')


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('organismo/<org:organismo>/', views.detalle_organismo),
    tie('organismo/<org:organismo>/estudio/', views.estudio_organismo),
    ]
