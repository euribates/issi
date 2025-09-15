#!/usr/bin/env python3

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def iff(entrada, opciones):
    op_if_true, op_if_false = opciones.split('|')
    if entrada:
        return mark_safe(op_if_true)
    else:
        return mark_safe(op_if_false)


@register.filter
def as_boolean(value):
    if value:
        return mark_safe('<strong class="green">☑ Si</strong>')
    else:
        return mark_safe('<strong class="red">☒ No</strong>')
