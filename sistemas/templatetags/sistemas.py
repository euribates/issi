#!/usr/bin/env python3

from html import escape

from django import template
from django.utils.safestring import mark_safe

from sistemas import links
from comun.templatetags.comun_filters import as_markdown


register = template.Library()

@register.filter
def as_codigo(sistema):
    url = sistema.url_detalle_sistema()
    return mark_safe(
        f'<a href="{url}" class="sistema-codigo">'
        f'{sistema.codigo}'
        '</a>'
        )
    

@register.filter
def as_nombre_sistema(sistema):
    return mark_safe(
        f'<span class="sistema-nombre">'
        f'{sistema.nombre_sistema}'
        '</span>'
        )


@register.filter
def as_descripcion(sistema):
    if not sistema.descripcion:
        return mark_safe(
            '<i class="bi bi-exclamation-diamond"></i>'
            '&nbsp;'
            '<i>Falta la descripción</i>'
            )
    return as_markdown(sistema.descripcion)


@register.filter
def as_finalidad(finalidad):
    if not finalidad:
        return mark_safe(
            '<i class="bi bi-exclamation-diamond"></i>'
            '&nbsp;'
            '<i>Falta definir la finalidad del S.I.</i>'
            )
    return as_markdown(finalidad)



@register.filter
def as_tema(tema):
    '''Representación textual, con HTML, del tema.
    '''
    url = links.a_tema(tema.pk)
    txt = tema.nombre_tema
    if tema.no_definido():
        icon = '<i class="bi bi-exclamation-diamond"></i> '
        klass = 'badge bg-danger text-white'
    else:
        icon = ''
        klass = 'badge bg-info text-white'
    return mark_safe(
        f'{icon}<span class="{klass}">'
        f'<a class="link-light text-decoration-none"'
        f' href="{url}">{txt}</a>'
        '</span>')


@register.filter
def as_familia(familia):
    '''Representación textual, con HTML, de la familia.
    '''
    url = links.a_detalle_familia(familia.pk)
    txt = familia.nombre_familia
    if familia.no_definida():
        icon = '<i class="bi bi-exclamation-diamond"></i> '
        klass = 'familia badge bg-danger text-white'
    else:
        icon = ''
        klass = 'familia badge bg-info text-white'
    return mark_safe(
        f'{icon}<span class="{klass}">'
        f'<a class="link-light text-decoration-none"'
        f' href="{url}">{txt}</a>'
        '</span>')


@register.filter
def as_status_icon(estado: str) -> str:
    return mark_safe(f'img/status/{estado}.svg')


@register.filter
def as_status_desc(estado: str) -> str:
    match estado:
        case 'green': 
            return 'Completo'
        case 'yellow':
            return 'Pendiente de algunos datos'
        case 'red':
            return 'Pendiente de algunos datos críticos'    
    return f'Error: estado {escape(estado)} desconocido'

