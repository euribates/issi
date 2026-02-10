#!/usr/bin/env python3

from django.urls import path

from . import views

app_name = 'juriscan'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('ficha/<int:num_ficha>/', views.ficha_juriscan),
    ]
