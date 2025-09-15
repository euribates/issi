#!/usr/bin/env python3

from django.urls import reverse_lazy

GOBCAN = 'www.gobiernodecanarias.org'


def a_organigrama(id_dircac):
    return 'https://{GOBCAN}/organigrama/{id_dircac}/'


def a_directorio():
    return reverse_lazy('directorio:index')


def a_detalle_organismo(id_organismo):
    return reverse_lazy('directorio:detalle_organismo', kwargs={
        'organismo': id_organismo,
        })
