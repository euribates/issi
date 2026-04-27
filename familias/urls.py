#!/usr/bin/env python3

from django.urls import path

from sistemas import converters  # noqa: F401
from . import views

app_name = 'familias'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('<fam:familia>/', views.detalle_familia),
    ]
