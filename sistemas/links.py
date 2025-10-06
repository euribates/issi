#!/usr/bin/env python3

from django.urls import reverse_lazy


def a_sistemas():
    return reverse_lazy('sistemas:index')


def a_alta_sistema():
    return reverse_lazy('sistemas:alta_sistema')


def a_detalle_sistema(id_sistema):
    return reverse_lazy('sistemas:detalle_sistema', kwargs={
        'sistema': id_sistema,
        })


def a_usuarios():
    return reverse_lazy('sistemas:listado_usuarios')


def a_detalle_usuario(login):
    return reverse_lazy('sistemas:detale_usuario', kwargs={
        'login': login,
        })

