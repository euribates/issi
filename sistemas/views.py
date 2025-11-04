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

from sistemas import filtersets
from directorio.models import Organismo
from directorio.models import Ente
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
    filterset = filtersets.SistemaFilter(
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
            sistema = Sistema.alta_sistema(
                nombre=data['nombre'],
                codigo=data['codigo'],
                proposito=data['proposito'],
                organismo=data['organismo'],
                tema=data['tema'],
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


def asignar_organismo(request, sistema):
    if request.method == "POST":
        form = forms.AsignarOrganismoForm(request.POST, instance=sistema)
        if form.is_valid():
            organismo = form.cleaned_data['organismo']
            from icecream import ic; ic(request.POST)
            from icecream import ic; ic(organismo)
            sistema.asignar_organismo(organismo)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarOrganismoForm(instance=sistema)
    return render(request, 'sistemas/asignar-organismo.html', {
        'titulo': f'Asignar {sistema} a organismo',
        'breadcrumbs': bc.asignar_organismo(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


def asignar_tema(request, sistema):
    if request.method == "POST":
        form = forms.AsignarTemaForm(request.POST, instance=sistema)
        if form.is_valid():
            sistema.asignar_tema(form.cleaned_data['tema'])
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarTemaForm(instance=sistema)
    return render(request, 'sistemas/asignar-tema.html', {
        'titulo': f'Asignar tema a {sistema}',
        'breadcrumbs': bc.asignar_tema(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


def editar_proposito(request, sistema):
    if request.method == "POST":
        form = forms.EditarPropositoForm(request.POST)
        if form.is_valid():
            sistema.proposito = form.cleaned_data['proposito']
            sistema.save()
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarPropositoForm(instance=sistema)
    return render(request, 'sistemas/editar-proposito.html', {
        'titulo': f'Editar proposito de {sistema}',
        'breadcrumbs': bc.editar_proposito(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


def detalle_sistema(request, sistema):
    return render(request, 'sistemas/detalle_sistema.html', {
        'titulo': f'Detalles {sistema}',
        'breadcrumbs': bc.detalle_sistema(sistema),
        'tab': 'sistemas',
        'sistema': sistema,
        'commands': cmd_sistemas(),
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


def listado_entes(request):
    return render(request, 'sistemas/listado_entes.html', {
        'titulo': 'Entes',
        'breadcrumbs': bc.entes(),
        'tab': 'entes',
        'entes': Ente.objects.all(),
        })


def detalle_ente(request, ente):
    return render(request, 'sistemas/detalle_ente.html', {
        'titulo': f'Detalles {ente}',
        'breadcrumbs': bc.detalle_ente(ente),
        'tab': 'entes',
        'ente': ente,
        'sistemas': (
            Sistema.objects
            .select_related('organismo')
            .filter(organismo__ruta__startswith=ente.organismo.ruta)
            .all()
            ),
        })



def listado_organismos(request):
    filterset = filtersets.OrganismoFilter(
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


def listado_activos(request):
    filterset = filtersets.ActivoFilter(
        request.GET,
        queryset=models.Activo.objects.all(),
        )
    return render(request, 'sistemas/listado-activos.html', {
        'titulo': "Listado de activos",
        'breadcrumbs': bc.activos(),
        'tab': 'activos',
        "filterset": filterset,
        })


def patch_organismos(request):
    datastar = request.GET.get('datastar')
    try:
        params = json.loads(datastar)
    except Exception as err:
        params = {
            'error': escape(repr(err)),
            }
    query = params.get("query")
    buff = [
        '<select name="organismo"'
        ' size="17"'
        ' class="form-control">',
        '<option value="">Sin asignar</option>'
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
