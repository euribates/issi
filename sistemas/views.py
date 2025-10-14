#!/usr/bin/env python3

from django.shortcuts import render

from . import models
from . import forms
from . import breadcrumbs as bc
from sistemas.filtersets import UsuarioFilter
from sistemas.filtersets import SistemaFilter
from directorio.filtersets import OrganismoFilter


def index(request, *args, **kwargs):
    sistemas = models.Sistema.objects.all()
    filterset = SistemaFilter(
        request.GET,
        queryset=sistemas,
        )
    return render(request, 'sistemas/index.html', {
        'titulo': 'Sistemas de información',
        'breadcrumbs': bc.sistemas(),
        'tab': 'sistemas',
        "filterset": filterset,
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
    filterset = UsuarioFilter(
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


def listado_organismos(request):
    filterset = OrganismoFilter(
        request.GET,
        queryset=models.Organismo.objects.all(),
        )
    return render(request, 'sistemas/listado_organismos.html', {
        'titulo': 'Organismos',
        'breadcrumbs': bc.organismos(),
        'tab': 'organismos',
        "filterset": filterset,
        })


def detalle_organismo(request, organismo):
    return render(request, 'sistemas/detalle_organismo.html', {
        'titulo': f'Detalles organismo {organismo}',
        'breadcrumbs': bc.detalle_organismo(organismo),
        'tab': 'organismos',
        'organismo': organismo,
        })


def listado_temas(request):
    return render(request, 'sistemas/listado_temas.html', {
        'titulo': 'Listado de temas (Áreas temáticas)',
        'breadcrumbs': bc.temas(),
        'tab': 'temas',
        'temas': models.Tema.objects.all(),
        })


def detalle_tema(request, tema):
    return render(request, 'sistemas/detalle_tema.html', {
        'titulo': str(tema),
        'breadcrumbs': bc.tema(tema),
        'tab': 'temas',
        'tema': tema,
        })

