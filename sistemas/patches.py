
# Patchs for datastar
import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q

from directorio.models import Empresa
from directorio.models import Organismo
from sistemas.models import Usuario
from sistemas.models import Sistema


@login_required
def get_datastar_parameter(request, name: str, default=None) -> str|None:
    datastar = request.GET.get('datastar', '')
    if datastar:
        params = json.loads(datastar)
        if name in params:
            return params[name]
    return default


@login_required
def patch_empresas(request):
    query = get_datastar_parameter(request, 'query')
    if query:
        empresas = Empresa.search_empresas(query)
    else:
        empresas = Empresa.objects.all()
    buff = [
        '<select name="empresa"'
        ' size="17"'
        ' class="form-control">',
        ]
    contador = empresas.count()
    selected = ' selected="selected"' if contador == 1 else ''
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
        f'<div id="contador">{contador}<div>'
        )

@login_required
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
        ]
    contador = organismos.count()
    selected = ' selected="selected"' if contador == 1 else ''
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
        f'<div id="contador">{contador}<div>'
        )


@login_required
def patch_sistemas(request):
    sistemas = Sistema.objects.all()
    total_sistemas = num_sistemas = sistemas.count()
    query = get_datastar_parameter(request, 'query')
    if query:
        sistemas = sistemas.filter(
            Q(nombre_sistema__icontains=query)
            | Q(codigo__icontains=query)
            | Q(tema__nombre_tema__icontains=query)
            )
        num_sistemas = sistemas.count()
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


