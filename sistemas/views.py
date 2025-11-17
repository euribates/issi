#!/usr/bin/env python3

import json
from html import escape
from functools import cache

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from comun.funcop import agrupa
from comun.bus import Bus
from . import breadcrumbs as bc
from . import forms
from . import links
from . import models
from . import diagnosis
from comun.commands import Command

from sistemas import filtersets
from directorio.models import Organismo
from directorio.models import Ente
from sistemas.models import Sistema
from sistemas.models import Usuario

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
    num_sistemas = sistemas.count()
    filterset = filtersets.SistemaFilter(
        request.GET,
        queryset=sistemas,
        )
    return render(request, 'sistemas/index.html', {
        'titulo': 'Sistemas de información',
        'breadcrumbs': bc.sistemas(),
        'commands': cmd_sistemas(),
        'tab': 'sistemas',
        'num_sistemas': num_sistemas,
        "filterset": filterset,
        })


def alta_sistema(request):
    if request.method == 'POST':
        form = forms.AltaSistemaForm(request.POST)
        if form.is_valid():
            data = form.as_dict()
            sistema = models.Sistema.alta_sistema(
                nombre=data['nombre'],
                codigo=data['codigo'],
                proposito=data['proposito'],
                organismo=data['organismo'],
                tema=data['tema'],
                )
            Bus(request).success(f'Añadido el sistema {sistema}')
            return redirect(sistema.url_detalle_sistema())
    else:
        form = forms.AltaSistemaForm()
    return render(request, 'sistemas/alta-sistema.html', {
        'titulo': 'Alta de un nuevo sistemas de información',
        'breadcrumbs': bc.alta_sistema(),
        'tab': 'sistemas',
        'form': form,
        })


def editar_sistema(request, sistema):
    if request.method == "POST":
        form = forms.EditarSistemaForm(request.POST, instance=sistema)
        if form.is_valid():
            form.save()
            Bus(request).success(
                f"El sistema de información {sistema}"
                f" ha sido modificado"
                )
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarSistemaForm(instance=sistema)
    return render(request, 'sistemas/editar-sistema.html', {
        'titulo': f'Editar {sistema}',
        'breadcrumbs': bc.editar_sistema(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })

def asignar_organismo(request, sistema):
    if request.method == "POST":
        form = forms.AsignarOrganismoForm(request.POST, instance=sistema)
        if form.is_valid():
            organismo = form.cleaned_data['organismo']
            sistema.asignar_organismo(organismo)
            Bus(request).success(
                f"El sistema de información {sistema}"
                f" ha sido asignado a {organismo}"
                )
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
            tema = sistema.asignar_tema(form.cleaned_data['tema'])
            Bus(request).success(
                f"El S.I. {sistema}"
                f" ha sido asignado al tema {tema}"
                )
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
            Bus(request).success(
                f"El propósito del S.I. {sistema}"
                " ha sido actualizado"
                )
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


def editar_descripcion(request, sistema):
    if request.method == "POST":
        form = forms.EditarDescripcionForm(request.POST, instance=sistema)
        if form.is_valid():
            form.save()
            Bus(request).success(
                f"La descripción del S.I. {sistema}"
                " ha sido actualizada"
                )
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarDescripcionForm(instance=sistema)
    return render(request, 'sistemas/editar-descripcion.html', {
        'titulo': f'Editar proposito de {sistema}',
        'breadcrumbs': bc.editar_proposito(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


def asignar_responsable(request, sistema):
    if request.method == "POST":
        form = forms.AsignarResponsableForm(request.POST)
        if form.is_valid():
            cometido = form.cleaned_data['cometido']
            usuario = form.cleaned_data['usuario']
            perfil = sistema.asignar_responsable(cometido, usuario)
            Bus(request).success(
                f"El usuario {perfil.usuario}"    
                f" a sido asignado como {perfil.get_cometido_display()}"
                f" del S.I. {perfil.sistema}"
                )
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarResponsableForm()
    return render(request, 'sistemas/asignar-responsable.html', {
        'titulo': f'Asignar responsable a {sistema}',
        'breadcrumbs': bc.asignar_responsable(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


def asignar_tema(request, sistema):
    if request.method == "POST":
        form = forms.AsignarTemaForm(request.POST, instance=sistema)
        if form.is_valid():
            tema = sistema.asignar_tema(form.cleaned_data['tema'])
            Bus(request).success(
                f"El S.I. {sistema}"
                f" ha sido asignado al tema {tema}"
                )
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


def asignar_icono(request, sistema):
    if request.method == "POST":
        form = forms.AsignarIconoForm(request.POST, request.FILES, instance=sistema)
        if form.is_valid():
            from icecream import ic; ic("form is valid")
            form.save()
            Bus(request).success(
                f"Se ha asignado un icono al S.I. {sistema}"
                )
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarIconoForm(instance=sistema)
    return render(request, 'sistemas/asignar-icono.html', {
        'titulo': f'Asignar icono a {sistema}',
        'breadcrumbs': bc.asignar_icono(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


def conmutar_campo(request, sistema, campo: str):
    """Conmutar el estado de un campo lógico.
    """
    if request.method == 'POST':
        form = forms.EstaSeguroForm(request.POST)
        if form.is_valid():
            setattr(sistema, campo, not getattr(sistema, campo))
            sistema.save()
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EstaSeguroForm()
    _field = Sistema._meta.get_field(campo)
    verbose_name = _field.verbose_name
    help_text = _field.help_text
    return render(request, 'sistemas/conmutar-campo.html', {
        'titulo': f'Cambiar el valor de {verbose_name}',
        'breadcrumbs': bc.conmutar_campo(sistema, campo, verbose_name),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        'campo': 'campo',
        'verbose_name': verbose_name,
        'help_text': help_text,
        })


def borrar_perfil(request, id_perfil: int):
    """Borrar un perfil.

    Después de ejecutar esta operación, el perfil
    indicado ya no existirá.

    No usamos conversores en este caso, porque queremos
    que la operación sea idempotente.

    Params:

        id_perfil (int): Clave primaria del perfil a borrar.
            Si no existe el perfil, no hace nada.
    """
    perfil = models.Perfil.load_perfil(id_perfil)
    if perfil:
        id_sistema = perfil.sistema.pk
        perfil.delete()
        Bus(request).success(
            f"El usuario {perfil.usuario}"    
            f" ha dejado de ser {perfil.get_cometido_display()}"
            f" del S.I. {perfil.sistema}"
            )
        return redirect(links.a_detalle_sistema(id_sistema))
    return redirect(links.a_sistemas())

    
def detalle_sistema(request, sistema):
    return render(request, 'sistemas/detalle-sistema.html', {
        'titulo': f'Detalles {sistema}',
        'breadcrumbs': bc.detalle_sistema(sistema),
        'tab': 'sistemas',
        'sistema': sistema,
        'diagnostico': diagnosis.DiagnosticoSistema(sistema),
        'commands': cmd_sistemas(),
        })


def listado_usuarios(request):
    messages.add_message(request, messages.INFO, "Hello world.")
    filterset = filtersets.UsuarioFilter(
        request.GET,
        queryset=models.Usuario.objects.all(),
        )
    return render(request, 'sistemas/listado-usuarios.html', {
        'titulo': 'Usuarios registrados en el sistema',
        'breadcrumbs': bc.usuarios(),
        'tab': 'usuarios',
        "filterset": filterset,
        })


def buscar_usuarios(request):
    return render(request, 'sistemas/buscar-usuarios.html', {
        'titulo': 'Buscar usuarios en pginas blancas',
        'subtitulo': 'Debe estar registrodo como usuario',
        'breadcrumbs': bc.usuarios(),
        'tab': 'usuarios',
        })


def detalle_usuario(request, usuario, *args, **kwargs):
    return render(request, 'sistemas/detalle-usuario.html', {
        'titulo': f'Detalles usuario {usuario}',
        'breadcrumbs': bc.detalle_usuario(usuario),
        'tab': 'usuarios',
        'usuario': usuario,
        })


def listado_entes(request):
    return render(request, 'sistemas/listado-entes.html', {
        'titulo': 'Entes',
        'breadcrumbs': bc.entes(),
        'tab': 'entes',
        'entes': Ente.objects.all(),
        })


def detalle_ente(request, ente):
    return render(request, 'sistemas/detalle-ente.html', {
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
    return render(request, 'sistemas/listado-organismos.html', {
        'titulo': 'Organismos',
        'breadcrumbs': bc.organismos(),
        'tab': 'organismos',
        "filterset": filterset,
        })


def detalle_organismo(request, organismo: Organismo):
    return render(request, 'sistemas/detalle-organismo.html', {
        'titulo': f'Detalles organismo {organismo}',
        'breadcrumbs': bc.detalle_organismo(organismo),
        'tab': 'organismos',
        'organismo': organismo,
        })


def listado_temas(request):
    temas = models.Tema.objects.with_counts().all()
    return render(request, 'sistemas/listado-temas.html', {
        'titulo': 'Listado de temas (Áreas temáticas)',
        'breadcrumbs': bc.temas(),
        'tab': 'temas',
        'agrupado': agrupa(temas, lambda _:_.inicial()),
        })


def detalle_tema(request, tema):
    return render(request, 'sistemas/detalle-tema.html', {
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


def pendientes(request):
    '''Dashboard de control de información ausente o incompleta.
    '''
    sin_tema = Sistema.objects.filter(tema='UNK').count()
    con_tema = Sistema.objects.exclude(tema='UNK').count()

    return render(request, 'sistemas/pendientes.html', {
        'titulo': "Listado de S.I. pendientes / incompletos",
        'breadcrumbs': bc.pendientes(),
        'sin_tema': sin_tema,
        'con_tema': con_tema,
        'tab': 'sistemas',
        })


def sistemas_sin_tema(request):
    '''Listado de sistemas que no tienen tema asignado.
    '''
    sistemas = Sistema.objects.filter(tema='UNK')
    return render(request, 'sistemas/sistemas-sin-tema.html', {
        'titulo': "Listado de S.I. pendientes de asignar tema",
        'breadcrumbs': bc.sistemas_sin_tema(),
        'tab': 'sistemas',
        'sistemas': sistemas,
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
        organismos = Organismo.search_organismos(query)
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


def patch_usuarios(request):
    datastar = request.GET.get('datastar')
    try:
        params = json.loads(datastar)
    except Exception as err:
        params = {
            'error': escape(repr(err)),
            }
    query = params.get("query")
    buff = [
        '<select name="usuario"'
        ' size="7"'
        ' class="form-control">',
        '<option value="">Sin asignar</option>'
        ]
    if query:
        usuarios = Usuario.search_usuarios(query)
    else:
        usuarios = Usuario.objects.all()[0:100]
    selected = ' selected'
    contador = usuarios.count()
    for usr in usuarios:
        buff.append(
            f'<option value="{usr.pk}"{selected}>'
            f'{usr}'
            '</option>'
            )
        selected = ''
    buff.append('</select>')
    result = '\n'.join(buff)
    return HttpResponse(
        f'<div id="control_usuarios">{result}</div>'
        f'<div id="contador">{contador}<div>'
        )
