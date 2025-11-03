#!/usr/bin/env python3

from django import template
from django.utils.safestring import mark_safe

from sistemas import links

register = template.Library()


@register.filter
def as_tema(tema):
    '''Representación textual, con HTML, del tema.
    '''
    url = links.a_tema(tema.pk)
    txt = tema.nombre_tema
    return mark_safe(f'<span class="tema"><a href="{url}">{txt}</a></span>')



@register.filter
def as_status_icon(estado):
    return mark_safe(f'img/status/{estado}.svg')
