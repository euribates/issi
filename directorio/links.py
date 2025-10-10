#!/usr/bin/env python3

from functools import cache

from django.urls import reverse_lazy

GOBCAN = 'www.gobiernodecanarias.org'

@cache
def a_organigrama(id_dircac: int) -> str:
    return f'https://{GOBCAN}/organigrama/?ou={id_dircac}/'


@cache
def a_directorio() -> str:
    return str(reverse_lazy('directorio:index'))


@cache
def a_detalle_organismo(id_organismo: int) -> str:
    return str(reverse_lazy('directorio:detalle_organismo', kwargs={
        'organismo': id_organismo,
        }))


@cache
def a_estudio_organismo(id_organismo: int) -> str:
    return str(reverse_lazy('directorio:estudio_organismo', kwargs={
        'organismo': id_organismo,
        }))
