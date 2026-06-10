#!/usr/bin/env python3

from django.urls import path
from django.urls import register_converter

from . import views
from . import converters

app_name = 'plan'


register_converter(converters.TareaConverter, 'task')


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('tareas/<task:tarea>/', views.detalle_tarea),
    tie('tareas/<task:tarea>/editar/', views.editar_tarea),
    tie('tareas/<task:tarea>/cerrar/', views.cerrar_tarea),
    ]
