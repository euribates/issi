#!/usr/bin/env python3

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def as_tema(tema):
    '''Representación textual, con HTML, del tema.
    '''
    return mark_safe(
        '<span class="badge text-bg-primary tema">'
        f'{tema.nombre_tema}'
        '</span>'
        )
