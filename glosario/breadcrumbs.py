#!/usr/bin/env python3

from comun.breadcrumbs import APPS
from . import links


def bc_issi():
    return APPS.step('ISSI', '/',)


def bc_glosario():
    return bc_issi().step('Glosario', links.a_glosario())
