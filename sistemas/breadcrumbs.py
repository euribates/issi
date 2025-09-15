#!/usr/bin/env python3

from comun.breadcrumbs import APPS
from . import links


def bc_issi():
    return APPS.step('ISSI', '/',)


def sistemas():
    return bc_issi().step('Sistemas', links.a_sistemas())


def alta_sistema():
    return sistemas().step(
        'Alta sistema',
        links.a_alta_sistema(),
        )

def detalle_sistema(sistema):
    return sistemas().step(
        str(sistema),
        links.a_detalle_sistema(sistema.pk),
        )
