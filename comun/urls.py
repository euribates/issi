#!/usr/bin/env python3

from django.urls import path

from . import views
from . import charts

app_name = 'comun'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    # tie('charts/doughnut/', views.doughnut),
    tie('charts/organismos.svg', charts.organismos),
    tie('lab/', charts.lab),
    tie('reset_password/', views.reset_password),
    tie('reset_password/ok/', views.reset_password_ok),
    tie('reset_password/error/', views.reset_password_error),
    tie('reset_password/check/<str:token>/', views.reset_password_check),
    ]
