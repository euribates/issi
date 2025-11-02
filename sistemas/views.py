#!/usr/bin/env python3

import json
from html import escape
from functools import cache

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from comun.funcop import agrupa
from . import breadcrumbs as bc
from . import forms
from . import links
from . import models
from comun.commands import Command

from sistemas.filtersets import UsuarioFilter
from sistemas.filtersets import SistemaFilter
from directorio.filtersets import OrganismoFilter
from directorio.models import Organismo
from sistemas.models import Sistema

@cache
def cmd_sistemas():
    return [
        Command(
            links.a_alta_sistema(),
            '⊞ Alta sistema',
            klass='warning',
            ),
        ]


def index(request, *args, **kwargs):
    sistemas = models.Sistema.objects.all()
    filterset = SistemaFilter(
        request.GET,
        queryset=sistemas,
        )
    return render(request, 'sistemas/index.html', {
        'titulo': 'Sistemas de información',
        'breadcrumbs': bc.sistemas(),
        'commands': cmd_sistemas(),
        'tab': 'sistemas',
        "filterset": filterset,
        })


def alta_sistema(request):
    if request.method == 'POST':
        form = forms.AltaSistemaForm(request.POST)
        if form.is_valid():
            data = form.as_dict()
            from icecream import ic; ic(data)
            sistema = Sistema.alta_sistema(
                nombre=data['nombre'],
                codigo=data['codigo'],
                proposito=data['proposito'],
                organismo=data['organismo'],
                )
            return redirect(sistema.url_detalle_sistema())
    else:
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
        queryset=Organismo.objects.all(),
        )
    return render(request, 'sistemas/listado_organismos.html', {
        'titulo': 'Organismos',
        'breadcrumbs': bc.organismos(),
        'tab': 'organismos',
        "filterset": filterset,
        })


def detalle_organismo(request, organismo: Organismo):
    return render(request, 'sistemas/detalle_organismo.html', {
        'titulo': f'Detalles organismo {organismo}',
        'breadcrumbs': bc.detalle_organismo(organismo),
        'tab': 'organismos',
        'organismo': organismo,
        })


def listado_temas(request):
    temas = models.Tema.objects.with_counts().all()
    return render(request, 'sistemas/listado_temas.html', {
        'titulo': 'Listado de temas (Áreas temáticas)',
        'breadcrumbs': bc.temas(),
        'tab': 'temas',
        'agrupado': agrupa(temas, lambda _:_.inicial()),
        })


def detalle_tema(request, tema):
    return render(request, 'sistemas/detalle_tema.html', {
        'titulo': str(tema),
        'breadcrumbs': bc.tema(tema),
        'tab': 'temas',
        'tema': tema,
        })


def patch_organismos(request):
    datastar = request.GET.get('datastar')
    try:
        params = json.loads(datastar)
    except Exception as err:
        params = {
            'error': escape(repr(err)),
            }
    from icecream import ic; ic(params)
    query = params.get("query")
    buff = [
        '<select name="id_organismo"'
        ' size="17"'
        ' class="form-control">'
        ]
    if query:
        organismos = Organismo.search(query)
    else:
        organismos = Organismo.objects.all()
    selected = ' selected'
    contador = organismos.count()
    for org in organismos:
        buff.append(
            f'<option value="{org.pk}"{selected}>'
            f'{org.nombre_organismo} {org.dir3}'
            '</option>'
            )
        selected = ''
    buff.append('</select>')
    result = '\n'.join(buff)
    return HttpResponse(
        f'<div id="control_organismos">{result}</div>'
        f'<div id="contador">{contador}<div>'
        )
