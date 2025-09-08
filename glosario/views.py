#!/usr/bin/env python3


from django.shortcuts import render

from . import models
from . import breadcrumbs


def index(request, *args, **kwargs):
    terminos = models.Termino.objects.all()
    return render(request, 'glosario/index.html', {
        'titulo': 'Términos',
        'breadcrumbs': breadcrumbs.bc_glosario(),
        'terminos': terminos,
        })

