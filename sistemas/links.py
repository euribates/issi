#!/usr/bin/env python3

from django.urls import reverse_lazy


def a_sistemas():
    return reverse_lazy('sistemas:index')


def a_alta_sistema():
    return reverse_lazy('sistemas:alta_sistema')

