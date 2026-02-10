#!/usr/bin/env python3

from django.urls import reverse_lazy


def _a(name: str, **kwargs) -> str:
    '''Azucar sintactico para definir funciones a_*.
    '''
    return str(reverse_lazy(name, kwargs=kwargs))


def a_juriscan() -> str:
    return _a('juriscan:index')


def a_ficha_juriscan(num_ficha: int):
    return _a('juriscan:ficha_juriscan', num_ficha=num_ficha)
