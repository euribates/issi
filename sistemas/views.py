#!/usr/bin/env python3

from django.shortcuts import render

from . import models
from . import forms
from . import breadcrumbs as bc
from . import filtersets


def index(request, *args, **kwargs):
    sistemas = models.Sistema.objects.all()
    return render(request, 'sistemas/index.html', {
        'titulo': 'Sistemas de información',
        'breadcrumbs': bc.sistemas(),
        'tab': 'sistemas',
        'sistemas': sistemas,
        })


def alta_sistema(request):
    form = forms.AltaSistemaForm()
    return render(request, 'sistemas/alta-sistema.html', {
        'titulo': 'Alta de un nuevo sistemas de información',
        'breadcrumbs': bc.alta_sistema(),
        'tab': 'sistemas',
        'form': form,
        })


def detalle_sistema(request, sistema):
    return render(request, 'sistemas/detalle_sistema.html', {
        'titulo': f'Detalles {sistema}',
        'breadcrumbs': bc.detalle_sistema(sistema),
        'tab': 'sistemas',
        'sistema': sistema,
        })


def listado_usuarios(request):
    filterset = filtersets.UsuarioFilter(
        request.GET,
        queryset=models.Usuario.objects.all(),
        )
    return render(request, 'sistemas/listado_usuarios.html', {
        'titulo': 'Usuarios registrados en el sistema',
        'breadcrumbs': bc.usuarios(),
        'tab': 'usuarios',
        "filterset": filterset,
        })


def buscar_usuarios(request):
    return render(request, 'sistemas/buscar_usuarios.html', {
        'titulo': 'Buscar usuarios en pginas blancas',
        'subtitulo': 'Debe estar registrodo como usuario',
        'breadcrumbs': bc.usuarios(),
        'tab': 'usuarios',
        })


def detalle_usuario(request, usuario, *args, **kwargs):
    return render(request, 'sistemas/detalle_usuario.html', {
        'titulo': f'Detalles usuario {usuario}',
        'breadcrumbs': bc.detalle_usuario(usuario),
        'tab': 'usuarios',
        'usuario': usuario,
        })
