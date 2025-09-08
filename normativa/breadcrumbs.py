#!/usr/bin/env python3

from comun.breadcrumbs import APPS
from . import links


def at_issi():
    return APPS.step('ISSI', '/',)


def at_normativa():
    return at_issi().step('normativa', links.a_normativa())
