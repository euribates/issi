#!/usr/bin/env python3

from django.shortcuts import render

from . import models
from . import forms
from . import breadcrumbs as bc


def index(request, *args, **kwargs):
    sistemas = models.Sistema.objects.all()
    return render(request, 'sistemas/index.html', {
        'titulo': 'Sistemas de información',
        'sistemas': sistemas,
        'breadcrumbs': bc.bc_sistemas(),
        })


def alta_sistema(request):
    form = forms.SistemaForm()
    return render(requst, 'sistemas/alta_sistema.html', {
        'titulo': 'Alta de un nuevo sistemas de información',
        'breadcrumbs': bc.alta_sistema(),
        })
