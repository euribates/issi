#!/usr/bin/env python3

from django.urls import path
from django.urls import register_converter

from . import views
from . import converters

app_name = 'plan'


register_converter(converters.BacklogConverter, 'blg')


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('backlog/<blg:backlog>/', views.editar_backlog),
    ]
