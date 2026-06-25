
# Patchs for datastar
import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from sistemas.models import Usuario
from comun.searchers import search_sistemas
from comun.searchers import search_empresas
from comun.searchers import search_organismos
from sistemas.models import Sistema


@login_required
def get_datastar_parameter(request, name: str, default=None) -> str|None:
    datastar = request.GET.get('datastar', '')
    if datastar:
        params = json.loads(datastar)
        if name in params:
            return params[name].strip()
    return default


@login_required
def patch_empresas(request):
    query = get_datastar_parameter(request, 'query')
    empresas = search_empresas(query)
    num_empresas = empresas.count()
    size = min(15, num_empresas)
    buff = [
        '<select name="empresa"'
        f' size="{size}"'
        ' class="form-control">',
        ]
    selected = ' selected="selected"' if num_empresas == 1 else ''
    for empresa in empresas:
        buff.append(
            f'<option value="{empresa.pk}"{selected}>'
            f'{empresa.nombre_empresa} (NIF {empresa.nif})'
            '</option>\n'
            )
        selected = ''
    buff.append('</select>')
    result = '\n'.join(buff)
    return HttpResponse(
        f'<div id="control_empresas">{result}</div>'
        f'<div id="contador">{num_empresas}<div>'
        )


@login_required
def patch_organismos(request):
    query = get_datastar_parameter(request, 'query')
    organismos = search_organismos(query)
    buff = [
        '<select name="organismo"'
        ' size="17"'
        ' class="form-control">',
        ]
    num_organismos = organismos.count()
    selected = ' selected="selected"' if num_organismos == 1 else ''
    for org in organismos:
        buff.append(
            f'<option value="{org.pk}"{selected}>'
            f'{org.nombre_organismo} (DIR3: {org.dir3})'
            '</option>\n'
            )
        selected = ''
    buff.append('</select>')
    result = '\n'.join(buff)
    return HttpResponse(
        f'<div id="control_organismos">{result}</div>'
        f'<div id="contador">{num_organismos}<div>'
        )


@login_required
def patch_sistemas(request):
    query = get_datastar_parameter(request, 'query')
    sistemas = search_sistemas(query)
    num_sistemas = sistemas.count()
    total_sistemas = Sistema.objects.all().count()
    return render(request, 'sistemas/includes/listado-sistemas.html', {
        'sistemas': sistemas,
        'num_sistemas': num_sistemas,
        'total_sistemas': total_sistemas,
        })


@login_required
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


@login_required
def patch_etapas(request):
    query = get_datastar_parameter(request, 'query')
    buff = [
        f'<input id="rb_etapa_{etapa}" type="radio" name="etapa" value="{etapa}">'
        f'<label for="rb_etapa_{etapa}">'
        f'{etapa.label}</label>\n'
        for etapa in Sistema.Etapas
        ]
    result = '<br>'.join(buff)
    return HttpResponse(f'<div id="dialog">{result}</div>')


