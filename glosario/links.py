#!/usr/bin/env python3

from django.urls import reverse_lazy


def a_glosario():
    return reverse_lazy('glosario:index')
