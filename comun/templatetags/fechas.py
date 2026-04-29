#!/usr/bin/env python3

from datetime import datetime as DateTime

from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def as_isoformat(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S%z')


@register.filter
def as_fecha(dt: DateTime) -> str:
    return dt.strftime('%A, %d/%B/%Y, a las %H:%M:%S %Z')


@register.filter
def es_datetime(dt: DateTime):
    return mark_safe(f'<time datetime="{as_isoformat(dt)}">{as_fecha(dt)}</time>')


@register.filter
def as_pasado(fecha: DateTime) -> str:
    """Retorna una representación textual aproximada del intervalo
    de tiempo, considerado desde el pasado.

    Parameters:

        fecha (DateTime): Fecha de referencia.

    Returns:

        (str) Descripción del intervalo de tiempo.

    """
    delta = timezone.now() - fecha
    days = delta.days
    seconds = delta.seconds
    match days:
        case days if days > 548:
            anios = round(delta.days / 365.0)
            legend = f'{anios} años'
        case days if days > 365:
            legend = 'un año'
        case days if days > 45:
            meses = round(delta.days / 30)
            legend = f'{meses} meses'
        case days if days > 28:
            legend = 'un mes'
        case days if days > 3:
            legend = f'{days} días'
        case 2:
            legend = 'anteayer'
        case 1:
            legend = 'ayer'
        case _:
            match seconds:
                case seconds if seconds > 3600:
                    hours = round(seconds / 3600)
                    legend = f'{hours} horas'
                case seconds if seconds > 60:
                    minutes = round(seconds / 60)
                    legend = f'{minutes} minutos'
                case _:
                    legend = f'{seconds} segundos'
    return mark_safe(
        f'<span class="as_pasado" title="{as_fecha(fecha)}">'
        f'<time datetime="{as_isoformat(fecha)}">'
        f'{legend}'
        '</time></span>'
        )




@register.filter
def as_created(dt: DateTime) -> str:
    str_date = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    return mark_safe(
        f'Creada el'
        f' <time datetime="{str_date}" title="{str_date}">'
        f'{as_pasado(dt)}</time>'
        )


@register.filter
def as_updated(dt: DateTime) -> str:
    str_date = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    return mark_safe(
        f'Modificado el'
        f' <time datetime="{str_date}" title="{str_date}">'
        f'{as_pasado(dt)}</time>'
        )
