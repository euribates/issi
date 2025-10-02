#!/usr/bin/env python3

from django.shortcuts import render

from . import models
from . import forms
from . import breadcrumbs as bc


def index(request, *args, **kwargs):
    sistemas = models.Sistema.objects.all()
    return render(request, 'sistemas/index.html', {
        'titulo': 'Sistemas de información',
        'breadcrumbs': bc.sistemas(),
        'tab': 'sistemas',
        'sistemas': sistemas,
        })


def alta_sistema(request):
    form = forms.SistemaForm()
    return render(requst, 'sistemas/alta_sistema.html', {
        'titulo': 'Alta de un nuevo sistemas de información',
        'breadcrumbs': bc.alta_sistema(),
        'tab': 'sistemas',
        })


def detalle_sistema(request, sistema):
    return render(request, 'sistemas/detalle_sistema.html', {
        'titulo': f'Detalles {sistema}',
        'breadcrumbs': bc.detalle_sistema(sistema),
        'tab': 'sistemas',
        'sistema': sistema,
        })


def listado_usuarios(request, *args, **kwargs):
    return render(request, 'sistemas/listado_usuarios.html', {
        'titulo': 'Usuarios registrados en el sistema',
        'breadcrumbs': bc.usuarios(),
        'tab': 'usuarios',
        'usuarios': models.Usuario.objects.all(),
        })
