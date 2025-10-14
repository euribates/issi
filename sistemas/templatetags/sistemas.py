#!/usr/bin/env python3

from django import template
from django.utils.safestring import mark_safe

from sistemas import links

register = template.Library()


@register.filter
def as_tema(tema):
    '''Representación textual, con HTML, del tema.
    '''
    return mark_safe(
        # '<span class="badge bg-primary text-bg-primary tema">'
        f'<a href="{links.a_tema(tema.pk)}">'
        f'{tema.nombre_tema}'
        '</a>'
        # '</span>'
        )
