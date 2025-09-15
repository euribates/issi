#!/usr/bin/env python3

from comun.breadcrumbs import APPS
from . import links


def issi():
    return APPS.step('ISSI', '/',)


def directorio():
    return issi().step('Directorio', links.a_directorio())


def detalle_organismo(organismo):
    return directorio().step(
        organismo.nombre_organismo,
        links.a_detalle_organismo(organismo.pk),
        )
