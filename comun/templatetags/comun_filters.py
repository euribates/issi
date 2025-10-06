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


@register.filter
def as_text_control(form, name):
    _field = form.fields[name]
    initial = _field.initial
    value = form.data.get(name, initial)
    _widget = _field.widget
    _widget.attrs['class'] = 'form-control'
    _widget.attrs['id'] = f'id_{name}'
    _widget.attrs['title'] = _field.help_text
    return _widget.render(name, value)


@register.filter
def as_checkbox(form, name):
    _field = form.fields[name]
    initial = _field.initial
    value = form.data.get(name, initial)
    _widget = _field.widget
    _widget.attrs['class'] = 'form-check-input'
    _widget.attrs['id'] = f'id_{name}'
    return _widget.render(name, value)
