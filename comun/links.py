#!/usr/bin/env python3

"""
Fichero para la creación de enlaces.

Todas las funciones públicas en este fichero deberían empezar por a_. Deden
devolver una string con la url relativa tal y como estén definidas 
en el fichero `urls.py`.

La función privada _a es una ayuda para escribir las funciones.

"""

from functools import cache

from django.urls import reverse_lazy


@cache
def _a(name: str, **kwargs) -> str:
    '''Azucar sintactico para definir funciones a_*.
    '''
    return str(reverse_lazy(f'comun:{name}', kwargs=kwargs))


def a_reset_password_check(token) -> str:
    return _a('reset_password_check', token=token.token)
