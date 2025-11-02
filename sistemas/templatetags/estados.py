#!/usr/bin/env python3

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def as_status_icon(estado):
    return mark_safe(f'img/status/{estado}.svg')
