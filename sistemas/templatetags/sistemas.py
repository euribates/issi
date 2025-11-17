#!/usr/bin/env python3

from django import template
from django.utils.safestring import mark_safe

from sistemas import links
from comun.templatetags.comun_filters import as_markdown


register = template.Library()


@register.filter
def as_descripcion(descripcion):
    if not descripcion:
        return mark_safe(
            '<i class="bi bi-exclamation-diamond"></i>'
            '&nbsp;'
            '<i>Falta la descripción</i>'
            )
    return as_markdown(descripcion)


@register.filter
def as_proposito(proposito):
    if not proposito:
        return mark_safe(
            '<i class="bi bi-exclamation-diamond"></i>'
            '&nbsp;'
            '<i>Falta definir el propósito del S.I.</i>'
            )
    return as_markdown(proposito)



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
def as_status_icon(estado):
    return mark_safe(f'img/status/{estado}.svg')


@register.filter
def as_status_desc(estado):
    match estado:
        case 'green': 
            return 'Completo'
        case 'yellow':
            return 'Pendiente de algunos datos'
        case 'red':
            return 'Pendiente de algunos datos críticos'
        case _:
            return _

