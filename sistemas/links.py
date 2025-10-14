#!/usr/bin/env python3

from django.urls import reverse_lazy


def a_sistemas() -> str:
    return str(reverse_lazy('sistemas:index'))


def a_alta_sistema() -> str:
    return str(reverse_lazy('sistemas:alta_sistema'))


def a_detalle_sistema(id_sistema) -> str:
    return str(reverse_lazy('sistemas:detalle_sistema', kwargs={
        'sistema': id_sistema,
        }))


def a_usuarios() -> str:
    return str(reverse_lazy('sistemas:listado_usuarios'))


def a_detalle_usuario(usuario) -> str:
    return str(reverse_lazy('sistemas:detalle_usuario', kwargs={
        'usuario': usuario,
        }))


def a_organismos() -> str:
    return str(reverse_lazy('sistemas:listado_organismos'))
    

def a_detalle_organismo(id_organismo) -> str:
    return str(reverse_lazy('sistemas:detalle_organismo', kwargs={
        'organismo': id_organismo,
        }))


def a_temas() -> str:
    return str(reverse_lazy('sistemas:listado_temas'))


def a_tema(id_tema:str) -> str:
    return str(reverse_lazy('sistemas:detalle_tema', kwargs={
        'tema': id_tema,
        }))
