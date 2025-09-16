#!/usr/bin/env python3

from django.urls import reverse_lazy

GOBCAN = 'www.gobiernodecanarias.org'


def a_organigrama(id_dircac):
    return f'https://{GOBCAN}/organigrama/?ou={id_dircac}/'


def a_directorio():
    return reverse_lazy('directorio:index')


def a_detalle_organismo(id_organismo):
    return reverse_lazy('directorio:detalle_organismo', kwargs={
        'organismo': id_organismo,
        })


def a_estudio_organismo(id_organismo):
    return reverse_lazy('directorio:estudio_organismo', kwargs={
        'organismo': id_organismo,
        })
