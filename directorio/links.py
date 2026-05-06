#!/usr/bin/env python3

from functools import cache

from django.urls import reverse_lazy

GOBCAN = 'www.gobiernodecanarias.org'

@cache
def a_organigrama(id_dircac: int) -> str:
    return f'https://{GOBCAN}/organigrama/?ou={id_dircac}/'


