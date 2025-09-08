#!/usr/bin/env python3

from django.urls import reverse_lazy


def a_normativa():
    return reverse_lazy('normativa:index')
