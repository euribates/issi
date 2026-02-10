#!/usr/bin/env python3

from comun.breadcrumbs import APPS
from . import links


def issi():
    return APPS.step('ISSI', '/',)


def juriscan():
    return issi().step('Juriscán', links.a_juriscan())


def ficha_juriscan(num_ficha: int):
    return juriscan().step(
        f'Ficha {num_ficha}',
        links.a_ficha_juriscan(num_ficha),
        )


