#!/usr/bin/env python3


from django.shortcuts import render

from . import models


def index(request, *args, **kwargs):
    terminos = models.Termino.objects.all()
    return render(request, 'glosario/index.html', {
        'titulo': 'Términos',
        'terminos': terminos,
        })

