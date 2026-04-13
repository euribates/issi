#!/usr/bin/env python3

from functools import cache
from collections import defaultdict

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from comun.error import errors
from comun.commands import Command
from comun.funcop import agrupa
from comun import graficas
from omnibus.bus import Bus

from directorio.models import Organismo
from sistemas import filtersets
from sistemas.models import Ente
from sistemas.importers import importar_sistemas_desde_fichero
from sistemas.models import Sistema

from . import breadcrumbs as bc
from . import diagnosis
from . import forms
from . import links
from . import models
from . import serializers

"""Vistas de sistemas.
"""

@cache
def cmd_sistemas():
    return [
        Command(
            links.a_importar_sistemas(),
            '<i class="bi bi-file-arrow-up"></i>'
            '&nbsp;Importar',
            klass='info',
            ),
        Command(
            links.a_exportar_sistemas(),
            '<i class="bi bi-file-arrow-down"></i>'
            '&nbsp;Exportar',
            klass='info',
            ),
        Command(
            links.a_alta_sistema(),
            '<i class="bi bi-plus-circle-fill"></i>'
            '&nbsp;Alta sistema',
            klass='warning',
            ),
        ]

@cache
def cmd_usuarios():
    return [
        Command(
            links.a_alta_usuario(),
            '⊞ Alta usuario',
            klass='warning',
            ),
        ]


@login_required
def index(request, *args, **kwargs):
    """Página de inicio de sistemas.
    """
    sistemas = (
        models.Sistema.objects
        .select_related('tema')
        .select_related('organismo')
        .order_by('-f_cambio')
        )
    total_sistemas = num_sistemas = sistemas.count()
    return render(request, 'sistemas/index.html', {
        'titulo': f'Hay {num_sistemas} sistemas de información',
        'subtitulo': 'Identificados en el sistema', 
        'breadcrumbs': bc.bc_sistemas(),
        'commands': cmd_sistemas(),
        'tab': 'sistemas',
        'sistemas': sistemas,
        'num_sistemas': num_sistemas,
        'total_sistemas': total_sistemas,
        })


@login_required
def alta_sistema(request):
    if request.method == 'POST':
        form = forms.AltaSistemaForm(request.POST)
        if form.is_valid():
            data = form.as_dict()
            sistema = models.Sistema.alta_sistema(
                nombre_sistema=data['nombre_sistema'],
                codigo=data['codigo'],
                finalidad=data['finalidad'],
                organismo=data['organismo'],
                tema=data['tema'],
                )
            Bus(request).pub_nuevo_sistema(sistema)
            return redirect(sistema.url_detalle_sistema())
    else:
        form = forms.AltaSistemaForm()
    return render(request, 'sistemas/alta-sistema.html', {
        'titulo': 'Alta de un nuevo sistemas de información',
        'breadcrumbs': bc.bc_alta_sistema(),
        'tab': 'sistemas',
        'form': form,
        })


@login_required
def editar_sistema(request, sistema):
    if request.method == "POST":
        form = forms.EditarSistemaForm(request.POST, instance=sistema)
        if form.is_valid():
            diffs = form.diff_with(sistema)
            form.save()
            Bus(request).pub_sistema_modificado(sistema, **diffs)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarSistemaForm(instance=sistema)
    return render(request, 'sistemas/editar-sistema.html', {
        'titulo': f'Editar {sistema}',
        'breadcrumbs': bc.bc_editar_sistema(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def asignar_normativa(request, sistema):
    from django.http import HttpResponse
    return HttpResponse(" no implementado", content_type="text/plain")


@login_required
def desasignar_normativa(request, sistema, juriscan: int):
    from django.http import HttpResponse
    return HttpResponse(" no implementado", content_type="text/plain")



@login_required
def asignar_organismo(request, sistema):
    if request.method == "POST":
        form = forms.AsignarOrganismoForm(request.POST, instance=sistema)
        if form.is_valid():
            organismo = form.cleaned_data['organismo']
            sistema.asignar_organismo(organismo)
            Bus(request).sistema_asignado_organismo(sistema, organismo)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarOrganismoForm(instance=sistema)
    return render(request, 'sistemas/asignar-organismo.html', {
        'titulo': f'Asignar {sistema} a organismo',
        'breadcrumbs': bc.bc_asignar_organismo(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def asignar_familia(request, sistema):
    if request.method == "POST":
        form = forms.AsignarFamiliaForm(request.POST, instance=sistema)
        if form.is_valid():
            familia = sistema.asignar_familia(form.cleaned_data['familia'])
            Bus(request).pub_sistema_asignado_familia(sistema, familia)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarFamiliaForm(instance=sistema)
    return render(request, 'sistemas/asignar-familia.html', {
        'titulo': f'Asignar familia a {sistema}',
        'breadcrumbs': bc.bc_asignar_familia(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def editar_finalidad(request, sistema):
    if request.method == "POST":
        form = forms.EditarFinalidadForm(request.POST)
        if form.is_valid():
            finalidad = form.cleaned_data['finalidad']
            if finalidad != sistema.finalidad:
                sistema.save(update_fields=['finalidad'])
                Bus(request).pub_sistema_editar_finalidad(sistema, finalidad)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarFinalidadForm(instance=sistema)
    return render(request, 'sistemas/editar-finalidad.html', {
        'titulo': f'Editar finalidad de {sistema}',
        'breadcrumbs': bc.bc_editar_finalidad(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })

@login_required
def editar_codigo(request, sistema):
    if request.method == "POST":
        form = forms.EditarCodigoForm(request.POST, instance=sistema)
        if form.is_valid():
            sistema.codigo = form.cleaned_data['codigo']
            sistema.save(update_fields=['codigo'])
            Bus(request).pub_sistema_editar_codigo(sistema, sistema.codigo)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarCodigoForm(instance=sistema)
    return render(request, 'sistemas/editar-codigo.html', {
        'titulo': f'Editar código de {sistema}',
        'breadcrumbs': bc.bc_editar_codigo(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def editar_nombre(request, sistema):
    if request.method == "POST":
        form = forms.EditarNombreForm(request.POST, instance=sistema)
        if form.is_valid():
            sistema.nombre_sistema = form.cleaned_data['nombre_sistema']
            sistema.save(update_fields=['nombre_sistema'])
            Bus(request).pub_sistema_editar_nombre(sistema, sistema.nombre)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarNombreForm(instance=sistema)
    return render(request, 'sistemas/editar-nombre.html', {
        'titulo': f'Editar nombre de {sistema}',
        'breadcrumbs': bc.bc_editar_nombre(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def editar_url(request, sistema):
    if request.method == "POST":
        form = forms.EditarURLForm(request.POST, instance=sistema)
        if form.is_valid():
            sistema.url = form.cleaned_data['url']
            sistema.save(update_fields=['url'])
            Bus(request).pub_sistema_editar_url(sistema, sistema.url)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarURLForm(instance=sistema)
    return render(request, 'sistemas/editar-url.html', {
        'titulo': f'Editar URL de {sistema}',
        'breadcrumbs': bc.bc_editar_url(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def editar_descripcion(request, sistema):
    if request.method == "POST":
        form = forms.EditarDescripcionForm(request.POST, instance=sistema)
        if form.is_valid():
            sistema.descripcion = form.cleaned_data['descripcion']
            sistema.save(update_fields=['descripcion'])
            Bus(request).pub_sistema_editar_descripcion(sistema, sistema.descripcion)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarDescripcionForm(instance=sistema)
    return render(request, 'sistemas/editar-descripcion.html', {
        'titulo': f'Editar finalidad de {sistema}',
        'breadcrumbs': bc.bc_editar_finalidad(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def asignar_responsable(request, sistema):
    if request.method == "POST":
        form = forms.AsignarResponsableForm(request.POST)
        if form.is_valid():
            cometido = form.cleaned_data['cometido']
            usuario = form.cleaned_data['usuario']
            perfil = sistema.asignar_responsable(cometido, usuario)
            Bus(request).pub_sistema_asignar_responsable(sistema, perfil)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarResponsableForm()
    return render(request, 'sistemas/asignar-responsable.html', {
        'titulo': f'Asignar responsable a {sistema}',
        'breadcrumbs': bc.bc_asignar_responsable(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def asignar_tema(request, sistema):
    if request.method == "POST":
        form = forms.AsignarTemaForm(request.POST, instance=sistema)
        if form.is_valid():
            tema = sistema.asignar_tema(form.cleaned_data['tema'])
            Bus(request).pub_sistema_asignar_materia(sistema, tema)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarTemaForm(instance=sistema)
    return render(request, 'sistemas/asignar-tema.html', {
        'titulo': f'Asignar tema a {sistema}',
        'breadcrumbs': bc.bc_asignar_tema(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


@login_required
def asignar_icono(request, sistema):
    if request.method == "POST":
        form = forms.AsignarIconoForm(request.POST, request.FILES, instance=sistema)
        if form.is_valid():
            form.save()
            Bus(request).pub_sistema_asignar_icono(sistema)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarIconoForm(instance=sistema)
    return render(request, 'sistemas/asignar-icono.html', {
        'titulo': f'Asignar icono a {sistema}',
        'tab': 'sistemas',
        'breadcrumbs': bc.bc_asignar_icono(sistema),
        'form': form,
        'sistema': sistema,
        })


def labo(request, *args, **kwargs):
    import pandas as pd
    from plotly.offline import plot
    import plotly.express as px
    from datetime import date as Date

    data = [
        {
            'Project': 'Alpha Flight',
            'Start': Date(2026, 3, 1),
            'Finish': Date(2026, 3, 16),
            'Responsible': 'Department H',
        },
        {
            'Project': 'Reborn',
            'Start': Date(2026, 3, 7),
            'Finish': Date(2026, 4, 6),
            'Responsible': 'Steve Rogres',
        },
        ]
    df = pd.DataFrame(data)
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Project",
        color="Responsible",
        )
    fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type='div')
    from comun.graficas import PolarChart
    radar = PolarChart('ISC')
    radar.add_axis('Seguridad', label='S')
    radar.add_axis('Calidad', label='C')
    radar.add_axis('Interoperabilidad', label='I')
    radar.add_axis('Personal', label='P')
    radar.add_axis('Matraka', label='M')
    radar.add_serie([12, 2.5, 12, 8, 17], label="ISSI")
    return render(request, "sistemas/labo.html", {
        'titulo': 'Labo sistemas',
        'chart': radar,
        'plot_div': gantt_plot,
        })



def create_graph(respuestas):
    radar = graficas.Radar('ISC')
    for eje in models.Eje.objects.all():
        radar.add_axis(eje.nombre_eje)
    dataset = defaultdict(list)
    for r in respuestas.all():
        key = r.opcion.pregunta.eje
        dataset[key].append(float(r.opcion.valor))
    for eje, values in dataset.items():
        if values:
            value = sum(values) * float(eje.influencia) / eje.num_preguntas
        else:
            value = 0.0
        radar.add_value(eje.nombre_eje, value, color=eje.color)
    return radar
        

    


#    series = [
#        (r.opcion.pregunta.eje_id, )
#        ]
#    labels = []
#    values = []
#    for eje_id, eje in ejes.items():
#        labels.append(eje.nombre_eje)
#        _values = [value for eje, value in series if eje == eje_id]
#        if eje.num_preguntas > 0:
#            value = sum(_values) * float(eje.influencia) / eje.num_preguntas
#        else:
#            value = 0.0
#        values.append(value)
#        pal = [
#            '#FFF09C80',
#            '#FFF09C80',
#            '#E6E6FA80',
#            '#FFB6C180',
#            '#FFDAB980',
#            '#C5E5E880',
#            ]
#
#
#    chart = MyBarGraph()
#    chart.data.label = "ISC"
#    return chart.get()


@login_required
def cuestionario_sistema(request, sistema):
    preguntas = models.Pregunta.objects.all()
    respuestas = sistema.respuestas.all()
    return render(request, 'sistemas/cuestionario-sistema.html', {
        'titulo': f'Cuestionario específico para {sistema}',
        'tab': 'sistemas',
        'breadcrumbs': bc.bc_cuestionario_sistema(sistema),
        'sistema': sistema,
        'preguntas': preguntas,
        'num_preguntas': preguntas.count(),
        'chartJSON': create_graph(respuestas),
        })


@login_required
def conmutar_campo(request, sistema, campo: str):
    """Conmutar el estado de un campo lógico.
    """
    if request.method == 'POST':
        form = forms.EstaSeguroForm(request.POST)
        if form.is_valid():
            setattr(sistema, campo, not getattr(sistema, campo))
            sistema.save()
            Bus(request).pub_sistema_conmutar_campo(sistema, campo)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EstaSeguroForm()
    _field = Sistema._meta.get_field(campo)
    verbose_name = _field.verbose_name
    help_text = _field.help_text
    return render(request, 'sistemas/conmutar-campo.html', {
        'titulo': f'Cambiar el valor de {verbose_name}',
        'breadcrumbs': bc.bc_conmutar_campo(sistema, campo, verbose_name),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        'campo': 'campo',
        'valor': getattr(sistema, campo),
        'verbose_name': verbose_name,
        'help_text': help_text,
        'url_cancel': links.a_detalle_sistema(sistema),
        })


@login_required
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
        Bus(request).pub_perfil_borrado(perfil)
        return redirect(links.a_detalle_sistema(id_sistema))
    return redirect(links.a_sistemas())

    
def isc_chart(sistema):
    from comun.graficas import PolarChart
    import random
    polar = PolarChart(f'ISC {sistema.codigo}', max_value=25)
    polar.add_axis('C', 'Calidad')
    polar.add_axis('D', 'Protección de datos')
    polar.add_axis('I', 'Interoperabilidad')
    polar.add_axis('P', 'Personas')
    polar.add_axis('R', 'Reutilización')
    polar.add_axis('S', 'Seguridad')
    data = [
        random.randint(0, 18),
        random.randint(0, 18),
        random.randint(0, 18),
        random.randint(0, 10),
        random.randint(0, 18),
        random.randint(0, 18),
        ]
    polar.add_serie(data, label=str(sistema))
    return polar


@login_required
def backlog_sistema(request, sistema):
    form = forms.BacklogForm(sistema=sistema)
    return render(request, 'sistemas/backlog-sistema.html', {
        'titulo': f'Backlog {sistema}',
        'commands': cmd_sistemas(),
        'breadcrumbs': bc.bc_backlog_sistema(sistema),
        'tab': 'sistemas',
        'sistema': sistema,
        'form': form,
        })


@login_required
def crear_backlog(request, sistema):
    if request.method == 'POST':
        form = forms.BacklogForm(request.POST, sistema=sistema)
        if form.is_valid():
            task = form.save()
            sistema.touch()
            Bus(request).pub_alta_backlog(task)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.BacklogForm(sistema=sistema)
    return render(request, 'sistemas/crear-backlog.html', {
        'titulo': f'Añadir item al Backlog de {sistema}',
        'commands': cmd_sistemas(),
        'breadcrumbs': bc.bc_crear_backlog(sistema),
        'tab': 'sistemas',
        'sistema': sistema,
        'form': form,
        })



@login_required
def detalle_sistema(request, sistema):
    return render(request, 'sistemas/detalle-sistema.html', {
        'titulo': f'Detalles {sistema}',
        'commands': cmd_sistemas(),
        'breadcrumbs': bc.bc_detalle_sistema(sistema),
        'tab': 'sistemas',
        'sistema': sistema,
        'diagnostico': diagnosis.DiagnosticoSistema(sistema),
        'isc': isc_chart(sistema),
        })


@login_required
def listado_usuarios(request):
    messages.add_message(request, messages.INFO, "Hello world.")
    filterset = filtersets.UsuarioFilter(
        request.GET,
        queryset=models.Usuario.objects.all(),
        )
    return render(request, 'sistemas/listado-usuarios.html', {
        'titulo': 'Usuarios registrados en el sistema',
        'breadcrumbs': bc.bc_usuarios(),
        'tab': 'usuarios',
        'commands': cmd_usuarios(),
        "filterset": filterset,
        })


@login_required
def buscar_usuarios(request):
    return render(request, 'sistemas/buscar-usuarios.html', {
        'titulo': 'Buscar usuarios en pginas blancas',
        'subtitulo': 'Debe estar registrodo como usuario',
        'breadcrumbs': bc.bc_usuarios(),
        'tab': 'usuarios',
        })


@login_required
def alta_usuario(request, *args, **kwargs):
    return render(request, 'sistemas/alta-usuario.html', {
        'titulo': 'Dar de alta un nuevo usuario',
        'breadcrumbs': bc.bc_alta_usuario(),
        'tab': 'usuarios',
        })


@login_required
def alta_usuario_interno(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.AltaUsuarioInternoForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Bus(request).pub_nuevo_usuario(usuario)
            return redirect(links.a_detalle_usuario(usuario.pk))
    else:
        form = forms.AltaUsuarioInternoForm()
    return render(request, 'sistemas/alta-usuario-interno.html', {
        'titulo': 'Dar de alta un nuevo usuario (Interno)',
        'breadcrumbs': bc.bc_alta_usuario_interno(),
        'tab': 'usuarios',
        'form': form,
        })


@login_required
def alta_usuario_externo(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.AltaUsuarioExternoForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Bus(request).pub_nuevo_usuario(usuario)
            return redirect(links.a_detalle_usuario(usuario.pk))
    else:
        form = forms.AltaUsuarioExternoForm()
    return render(request, 'sistemas/alta-usuario-externo.html', {
        'titulo': 'Dar de alta un nuevo usuario (Externo)',
        'breadcrumbs': bc.bc_alta_usuario_externo(),
        'tab': 'usuarios',
        'form': form,
        })


@login_required
def detalle_usuario(request, usuario, *args, **kwargs):
    return render(request, 'sistemas/detalle-usuario.html', {
        'titulo': f'Detalles usuario {usuario}',
        'breadcrumbs': bc.bc_detalle_usuario(usuario),
        'tab': 'usuarios',
        'usuario': usuario,
        })


@login_required
def bar_sistemas2(request):
    from comun.charts import BarChart
    result = BarChart()
    for ente in Ente.objects.all():
        value = ente.sistemas_del_ente().count()
        match value:
            case _ if value == 0:
                color = '#CC3333'
            case _ if value < 3:
                color = '#FFA600'
            case _:
                color = '#87AB69'
        result.add_value(value or -0.5, ente.pk, color)
    return result

# def bar_sistemas2():
    # from pychartjs import BaseChart, ChartType, Color 

    # class MyBarGraph(BaseChart):

        # type = ChartType.Bar

        # class data:
            # label = "S.I."
            # data = [12, 19, 3, 17, 10]
            # backgroundColor = [
                # Color.Green,
                # Color.Red,
                # Color.Green,
                # Color.Green,
                # Color.Red,
                # ]

    # new_chart = BaseChart('bar')
    # new_chart.data.label = "Sistemas de información identificados"
    # items = [
        # (_e.pk, _e.sistemas_del_ente().count())
        # for _e in Ente.objects.all()
        # ]
        
    # new_chart.data.data = [_t[1] for _t in items]
    # new_chart.labels.vars = [_t[0] for _t in items]
    # new_chart.data.backgroundColor = [
        # Color.Orange if _t[1] <= 3 else Color.Green 
        # for _t in items
        # ]
    # return new_chart


@login_required
def listado_entes(request):
    chart = bar_sistemas2(request)
    return render(request, 'sistemas/listado-entes.html', {
        'titulo': 'Entes',
        'breadcrumbs': bc.bc_entes(),
        'tab': 'entes',
        'entes': Ente.objects.all(),
        'chart': chart.as_json(),
        })


@login_required
def detalle_ente(request, ente):
    return render(request, 'sistemas/detalle-ente.html', {
        'titulo': f'Detalles {ente}',
        'breadcrumbs': bc.bc_detalle_ente(ente),
        'tab': 'entes',
        'ente': ente,
        'sistemas': (
            Sistema.objects
            .select_related('organismo')
            .filter(organismo__ruta__startswith=ente.organismo.ruta)
            .all()
            ),
        })


@login_required
def asignar_interlocutor(request, ente):
    if request.method == "POST":
        form = forms.AsignarInterlocutorForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            interlocutor = ente.asignar_interlocutor(usuario)
            Bus(request).pub_interlocutor_asignado(
                interlocutor.usuario,
                ente
                )
            return redirect(links.a_detalle_ente(ente.pk))
    else:
        form = forms.AsignarInterlocutorForm()
    return render(request, 'sistemas/asignar-interlocutor.html', {
        'titulo': f'Asignar interlocutor a {ente}',
        'breadcrumbs': bc.bc_asignar_interlocutor(ente),
        'tab': 'entes',
        'form': form,
        'ente': ente,
        })


@login_required
def liberar_interlocutor(request, ente, usuario):
    if request.method == "POST":
        form = forms.EstaSeguroForm(request.POST)
        if form.is_valid():
            Bus(request).pub_interlocutor_liberado(usuario, ente)
            ente.liberar_interlocutor(usuario)
            return redirect(links.a_detalle_ente(ente.pk))
    else:
        form = forms.EstaSeguroForm()
    return render(request, 'sistemas/liberar-interlocutor.html', {
        'titulo': f'Liberar interlocutor a {ente}',
        'breadcrumbs': bc.bc_liberar_interlocutor(ente, usuario),
        'tab': 'entes',
        'form': form,
        'ente': ente,
        'usuario': usuario,
        })


@login_required
def listado_organismos(request):
    filterset = filtersets.OrganismoFilter(
        request.GET,
        queryset=Organismo.objects.all(),
        )
    return render(request, 'sistemas/listado-organismos.html', {
        'titulo': 'Organismos',
        'breadcrumbs': bc.bc_organismos(),
        'tab': 'organismos',
        "filterset": filterset,
        })


@login_required
def detalle_organismo(request, organismo: Organismo):
    return render(request, 'sistemas/detalle-organismo.html', {
        'titulo': f'Detalles organismo {organismo}',
        'breadcrumbs': bc.bc_detalle_organismo(organismo),
        'tab': 'organismos',
        'organismo': organismo,
        })


@login_required
def listado_temas(request):
    temas = models.Tema.objects.with_counts().all()
    return render(request, 'sistemas/listado-temas.html', {
        'titulo': 'Listado de temas (Áreas temáticas)',
        'breadcrumbs': bc.bc_temas(),
        'tab': 'temas',
        'agrupado': agrupa(temas, lambda _:_.inicial()),
        })


@login_required
def detalle_tema(request, tema):
    return render(request, 'sistemas/detalle-tema.html', {
        'titulo': str(tema),
        'breadcrumbs': bc.bc_tema(tema),
        'tab': 'temas',
        'tema': tema,
        })


@login_required
def listado_familias(request):
    familias = models.Familia.objects.with_counts().all()
    return render(request, 'sistemas/listado-familias.html', {
        'titulo': 'Listado de familias (Áreas temáticas)',
        'breadcrumbs': bc.bc_familias(),
        'tab': 'familias',
        'familias': familias,
        })


@login_required
def detalle_familia(request, familia):
    return render(request, 'sistemas/detalle-familia.html', {
        'titulo': str(familia),
        'breadcrumbs': bc.bc_detalle_familia(familia),
        'tab': 'familias',
        'familia': familia,
        })


@login_required
def listado_preguntas(request):
    preguntas = models.Pregunta.objects.all()
    por_eje = agrupa(preguntas, lambda _p: _p.eje)
    return render(request, 'sistemas/listado-preguntas.html', {
        'titulo': 'Cuestionario de sistemas',
        'breadcrumbs': bc.bc_listado_preguntas(),
        'tab': 'cuestionario',
        'num_preguntas': preguntas.count(),
        'por_eje': por_eje,
        })


@login_required
def ver_pregunta(request, id_pregunta: int):
    pregunta = models.Pregunta.load_pregunta(id_pregunta)
    return render(request, 'sistemas/ver-pregunta.html', {
        'titulo': f'Pregunta {pregunta.pk}: {pregunta.texto_pregunta}',
        'breadcrumbs': bc.bc_ver_pregunta(pregunta),
        'tab': 'cuestionario',
        'pregunta': pregunta,
        })


@login_required
def alta_opcion(request, id_pregunta: int):
    pregunta = models.Pregunta.load_pregunta(id_pregunta)
    if request.method == 'POST':
        form = forms.AltaOpcionForm(request.POST, pregunta=pregunta)
        if form.is_valid():
            form.save()
            return redirect(links.a_ver_pregunta(pregunta.pk))
    else:
        form = forms.AltaOpcionForm(pregunta=pregunta)

    return render(request, 'sistemas/alta-opcion.html', {
        'titulo': f'Añadir opción a la pregunta {id_pregunta}',
        'breadcrumbs': bc.bc_alta_opcion(pregunta),
        'tab': 'cuestionario',
        'pregunta': pregunta,
        'form': form,
        })


@login_required
def listado_activos(request):
    filterset = filtersets.ActivoFilter(
        request.GET,
        queryset=models.Activo.objects.all(),
        )
    return render(request, 'sistemas/listado-activos.html', {
        'titulo': "Listado de activos",
        'breadcrumbs': bc.bc_activos(),
        'tab': 'activos',
        "filterset": filterset,
        })


@login_required
def pendientes(request):
    '''Dashboard de control de información ausente o incompleta.
    '''
    sin_tema = Sistema.objects.filter(tema='UNK').count()
    con_tema = Sistema.objects.exclude(tema='UNK').count()

    return render(request, 'sistemas/pendientes.html', {
        'titulo': "Listado de S.I. pendientes / incompletos",
        'breadcrumbs': bc.bc_pendientes(),
        'sin_tema': sin_tema,
        'con_tema': con_tema,
        'tab': 'sistemas',
        })


@login_required
def sistemas_sin_tema(request):
    '''Listado de sistemas que no tienen tema asignado.
    '''
    sistemas = Sistema.objects.filter(tema='UNK')
    return render(request, 'sistemas/sistemas-sin-tema.html', {
        'titulo': "Listado de S.I. pendientes de asignar tema",
        'breadcrumbs': bc.bc_sistemas_sin_tema(),
        'tab': 'sistemas',
        'sistemas': sistemas,
        })



def verificar_existencia_sistema(payload: dict) -> dict:
    '''Verifica si los datos a importar son consistentes con la BD.
    '''
    # Si indica UUID, este debe existir en la base de datos
    uuid_sistema = payload.get('uuid_sistema')
    if uuid_sistema:
        sistema = Sistema.load_sistema_por_uuid(uuid_sistema)
        if sistema:
            payload['sistema'] = sistema
        else:
            payload['errores'].append(errors.EI0010(uuid_sistema))
    ## El código debe ser único
    codigo = payload['codigo']
    sistema = Sistema.load_sistema_por_codigo(codigo)
    if sistema:
        payload['sistema'] = sistema
        payload['errores'].append(errors.EI0011(codigo))
    return payload


@login_required
def importar_sistemas(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.ODSFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES["archivo"]
            stream = archivo.read()
            sistemas = list(importar_sistemas_desde_fichero(stream))
            return render(request, 'sistemas/importar-sistemas-control.html', {
                'titulo': 'Importar sistemas - Selección',
                'commands': cmd_sistemas(),
                'tab': 'sistemas',
                'breadcrumbs': bc.bc_importar_sistemas(),
                'sistemas': sistemas,
                })

    else:
        form = forms.ODSFileForm()
    return render(request, 'sistemas/importar-sistemas.html', {
        'titulo': 'Importar sistemas',
        'commands': cmd_sistemas(),
        'tab': 'sistemas',
        'breadcrumbs': bc.bc_importar_sistemas(),
        'form': form,
        })



@login_required
def exportar_sistemas(request):
    return render(request, 'sistemas/exportar-sistemas.html', {
        'titulo': 'Exportar sistemas',
        'commands': cmd_sistemas(),
        'tab': 'sistemas',
        'breadcrumbs': bc.bc_exportar_sistemas(),
        'entes': Ente.objects.all(),
        })


@login_required
def exportar_sistemas_por_ente(request, ente: Ente):
    sistemas = ente.sistemas_del_ente()
    result = HttpResponse(content_type='text/csv')
    filename = f'sistemas-de-informacion-{ente.pk}.cvs'
    result.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    serializers.sistemas_a_csv(sistemas, result)
    return result


@login_required
def exportar_sistemas_todos(request):
    sistemas = Sistema.objects.all()
    result = HttpResponse(content_type='text/csv')
    result.headers['Content-Disposition'] ='attachment; filename="sistemas-de-informacion-CAC.cvs'
    serializers.sistemas_a_csv(sistemas, result)
    return result
