#!/usr/bin/env python3

from functools import cache
import io
import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Q

from . import breadcrumbs as bc
from . import diagnosis
from . import forms
from . import links
from . import models
from . import serializers

from comun.error import errors
from comun.bus import Bus
from comun.commands import Command
from comun.funcop import agrupa

from directorio.models import Organismo
from sistemas import filtersets
from sistemas.models import Ente
from sistemas.models import importar_sistemas_desde_fichero
from sistemas.models import Sistema
from sistemas.models import Usuario

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



def index(request, *args, **kwargs):
    """Página de inicio de sistemas.
    """
    sistemas = (
        models.Sistema.objects
        .select_related('tema')
        .select_related('organismo')
        .order_by('-f_cambio')
        )
    num_sistemas = sistemas.count()
    return render(request, 'sistemas/index.html', {
        'titulo': 'Sistemas de información',
        'breadcrumbs': bc.sistemas(),
        'commands': cmd_sistemas(),
        'tab': 'sistemas',
        'sistemas': sistemas,
        'num_sistemas': num_sistemas,
        })


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


def asignar_normativa(request, sistema):
    from django.http import HttpResponse
    return HttpResponse(" no implementado", content_type="text/plain")


def desasignar_normativa(request, sistema, juriscan: int):
    from django.http import HttpResponse
    return HttpResponse(" no implementado", content_type="text/plain")



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



def asignar_familia(request, sistema):
    if request.method == "POST":
        form = forms.AsignarFamiliaForm(request.POST, instance=sistema)
        if form.is_valid():
            familia = sistema.asignar_familia(form.cleaned_data['familia'])
            Bus(request).success(
                f"El S.I. {sistema}"
                f" ha sido asignado a la familia {familia}"
                )
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarFamiliaForm(instance=sistema)
    return render(request, 'sistemas/asignar-familia.html', {
        'titulo': f'Asignar familia a {sistema}',
        'breadcrumbs': bc.asignar_familia(sistema),
        'tab': 'sistemas',
        'form': form,
        'sistema': sistema,
        })


def editar_finalidad(request, sistema):
    if request.method == "POST":
        form = forms.EditarFinalidadForm(request.POST)
        if form.is_valid():
            sistema.finalidad = form.cleaned_data['finalidad']
            sistema.save()
            Bus(request).success(
                f"El propósito del S.I. {sistema}"
                " ha sido actualizado"
                )
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.EditarFinalidadForm(instance=sistema)
    return render(request, 'sistemas/editar-finalidad.html', {
        'titulo': f'Editar finalidad de {sistema}',
        'breadcrumbs': bc.editar_finalidad(sistema),
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
        'titulo': f'Editar finalidad de {sistema}',
        'breadcrumbs': bc.editar_finalidad(sistema),
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
                f" ha sido asignado como {perfil.get_cometido_display()}"
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
            form.save()
            Bus(request).success(
                f"Se ha asignado un icono al S.I. {sistema}"
                )
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.AsignarIconoForm(instance=sistema)
    return render(request, 'sistemas/asignar-icono.html', {
        'titulo': f'Asignar icono a {sistema}',
        'tab': 'sistemas',
        'breadcrumbs': bc.asignar_icono(sistema),
        'form': form,
        'sistema': sistema,
        })



def create_graph(respuestas):
    from pychartjs import BaseChart, ChartType
    ejes = { eje.pk: eje for eje in models.Eje.objects.all() }
    series = [
        (r.opcion.pregunta.eje_id, float(r.opcion.valor))
        for r in respuestas.all()
        ]
    labels = []
    values = []
    for eje_id, eje in ejes.items():
        labels.append(eje.nombre_eje)
        _values = [value for eje, value in series if eje == eje_id]
        if eje.num_preguntas > 0:
            value = sum(_values) * float(eje.influencia) / eje.num_preguntas
        else:
            value = 0.0
        values.append(value)
    
    class MyBarGraph(BaseChart):

        type = ChartType.Radar

        class labels:
            group = labels

        class data:
            data = values
            label = labels
            backgroundColor = [
                '#FFF09C80',
                '#FFF09C80',
                '#E6E6FA80',
                '#FFB6C180',
                '#FFDAB980',
                '#C5E5E880',
                ]


    chart = MyBarGraph()
    chart.data.label = "ISC"
    return chart.get()


def cuestionario_sistema(request, sistema):
    preguntas = models.Pregunta.objects.all()
    respuestas = sistema.respuestas.all()
    return render(request, 'sistemas/cuestionario-sistema.html', {
        'titulo': f'Cuestionario específico para {sistema}',
        'tab': 'sistemas',
        'breadcrumbs': bc.cuestionario_sistema(sistema),
        'sistema': sistema,
        'preguntas': preguntas,
        'num_preguntas': preguntas.count(),
        'chartJSON': create_graph(respuestas),
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
        'valor': getattr(sistema, campo),
        'verbose_name': verbose_name,
        'help_text': help_text,
        'url_cancel': links.a_detalle_sistema(sistema),
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
        'commands': cmd_usuarios(),
        "filterset": filterset,
        })


def buscar_usuarios(request):
    return render(request, 'sistemas/buscar-usuarios.html', {
        'titulo': 'Buscar usuarios en pginas blancas',
        'subtitulo': 'Debe estar registrodo como usuario',
        'breadcrumbs': bc.usuarios(),
        'tab': 'usuarios',
        })


def alta_usuario(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.AltaUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Bus(request).success(
                f"Se ha dado de alta al usuario {usuario}"
                )
            return redirect(links.a_detalle_usuario(usuario.pk))
    else:
        form = forms.AltaUsuarioForm()
    return render(request, 'sistemas/alta-usuario.html', {
        'titulo': 'Dar de alta un nuevo usuario',
        'breadcrumbs': bc.usuarios(),
        'tab': 'usuarios',
        'form': form,
        })


def detalle_usuario(request, usuario, *args, **kwargs):
    return render(request, 'sistemas/detalle-usuario.html', {
        'titulo': f'Detalles usuario {usuario}',
        'breadcrumbs': bc.detalle_usuario(usuario),
        'tab': 'usuarios',
        'usuario': usuario,
        })

def bar_sistemas2():
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


def listado_entes(request):
    chart = bar_sistemas2()
    return render(request, 'sistemas/listado-entes.html', {
        'titulo': 'Entes',
        'breadcrumbs': bc.entes(),
        'tab': 'entes',
        'entes': Ente.objects.all(),
        'chart': chart.as_json(),
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


def asignar_interlocutor(request, ente):
    if request.method == "POST":
        form = forms.AsignarInterlocutorForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            interlocutor = ente.asignar_interlocutor(usuario)
            Bus(request).success(
                f"El usuario {interlocutor.usuario}"    
                " ha sido asignado como interlocutor"
                f" del ente {ente}"
                )
            return redirect(links.a_detalle_ente(ente.pk))
    else:
        form = forms.AsignarInterlocutorForm()
    return render(request, 'sistemas/asignar-interlocutor.html', {
        'titulo': f'Asignar interlocutor a {ente}',
        'breadcrumbs': bc.asignar_interlocutor(ente),
        'tab': 'entes',
        'form': form,
        'ente': ente,
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


def listado_familias(request):
    familias = models.Familia.objects.with_counts().all()
    return render(request, 'sistemas/listado-familias.html', {
        'titulo': 'Listado de familias (Áreas temáticas)',
        'breadcrumbs': bc.familias(),
        'tab': 'familias',
        'familias': familias,
        })


def detalle_familia(request, familia):
    return render(request, 'sistemas/detalle-familia.html', {
        'titulo': str(familia),
        'breadcrumbs': bc.detalle_familia(familia),
        'tab': 'familias',
        'familia': familia,
        })


def listado_preguntas(request):
    preguntas = models.Pregunta.objects.all()
    por_eje = agrupa(preguntas, lambda _p: _p.eje)
    return render(request, 'sistemas/listado-preguntas.html', {
        'titulo': 'Cuestionario de sistemas',
        'breadcrumbs': bc.listado_preguntas(),
        'tab': 'cuestionario',
        'num_preguntas': preguntas.count(),
        'por_eje': por_eje,
        })


def ver_pregunta(request, id_pregunta: int):
    pregunta = models.Pregunta.load_pregunta(id_pregunta)
    return render(request, 'sistemas/ver-pregunta.html', {
        'titulo': f'Pregunta {pregunta.pk}: {pregunta.texto_pregunta}',
        'breadcrumbs': bc.ver_pregunta(pregunta),
        'tab': 'cuestionario',
        'pregunta': pregunta,
        })


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
        'breadcrumbs': bc.alta_opcion(pregunta),
        'tab': 'cuestionario',
        'pregunta': pregunta,
        'form': form,
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


# Patchs for datastar


def get_datastar_parameter(request, name: str, default=None) -> str|None:
    datastar = request.GET.get('datastar', '')
    if datastar:
        params = json.loads(datastar)
        if name in params:
            return params[name]
    return default


def patch_organismos(request):
    query = get_datastar_parameter(request, 'query')
    if query:
        organismos = Organismo.search_organismos(query)
    else:
        organismos = Organismo.objects.all()
    buff = [
        '<select name="organismo"'
        ' size="17"'
        ' class="form-control">',
        '<option value="">Sin asignar</option>'
        ]
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


def patch_sistemas(request):
    sistemas = Sistema.objects.all()
    query = get_datastar_parameter(request, 'query')
    if query:
        sistemas = sistemas.filter(
            Q(nombre_sistema__icontains=query)
            | Q(codigo__icontains=query)
            | Q(tema__nombre_tema__icontains=query)
            )
    return render(request, 'sistemas/includes/listado-sistemas.html', {
        'sistemas': sistemas,
        })


def patch_usuarios(request):
    query = get_datastar_parameter(request, 'query')
    if query:
        usuarios = Usuario.search_usuarios(query)
    else:
        usuarios = Usuario.objects.all()[0:100]
    buff = [
        '<select name="usuario"'
        ' size="7"'
        ' class="form-control">',
        '<option value="">Sin asignar</option>'
        ]
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


def importar_sistemas(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.CVSFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES["archivo"]
            stream = io.StringIO(archivo.read().decode('utf-8'))
            results = [
                verificar_existencia_sistema(_sis)
                for _sis in importar_sistemas_desde_fichero(stream)
                ]
            return render(request, 'sistemas/importar-sistemas-control.html', {
                'titulo': 'Importar sistemas',
                'commands': cmd_sistemas(),
                'tab': 'sistemas',
                'breadcrumbs': bc.importar_sistemas(),
                'results': results,
                })

    else:
        form = forms.CVSFileForm()
    return render(request, 'sistemas/importar-sistemas.html', {
        'titulo': 'Importar sistemas',
        'commands': cmd_sistemas(),
        'tab': 'sistemas',
        'breadcrumbs': bc.importar_sistemas(),
        'form': form,
        })



def exportar_sistemas(request):
    return render(request, 'sistemas/exportar-sistemas.html', {
        'titulo': 'Exportar sistemas',
        'commands': cmd_sistemas(),
        'tab': 'sistemas',
        'breadcrumbs': bc.exportar_sistemas(),
        'entes': Ente.objects.all(),
        })


def exportar_sistemas_por_ente(request, ente: Ente):
    sistemas = ente.sistemas_del_ente()
    result = HttpResponse(content_type='text/csv')
    filename = f'sistemas-de-informacion-{ente.pk}.cvs'
    result.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    serializers.sistemas_a_csv(sistemas, result)
    return result


def exportar_sistemas_todos(request):
    sistemas = Sistema.objects.all()
    result = HttpResponse(content_type='text/csv')
    result.headers['Content-Disposition'] ='attachment; filename="sistemas-de-informacion-CAC.cvs'
    serializers.sistemas_a_csv(sistemas, result)
    return result
