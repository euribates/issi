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
        str(sistema.codigo),
        links.a_detalle_sistema(sistema.pk),
        )

def asignar_tema(sistema):
    return detalle_sistema(sistema).step(
        "Asignar tema",
        links.a_asignar_tema(sistema.pk),
        )


def usuarios():
    return bc_issi().step('Usuarios', links.a_usuarios())


def detalle_usuario(usuario):
    return usuarios().step(
        usuario.login,
        links.a_detalle_usuario(usuario.login),
        )


def organismos():
    return bc_issi().step('Organismos', links.a_organismos())


def detalle_organismo(organismo):
    return organismos().step(
        organismo.nombre_organismo,
        links.a_detalle_organismo(organismo.pk),
        )


def temas():
    return bc_issi().step('Temas', links.a_temas())


def tema(t):
    return temas().step(str(t), links.a_tema(t.id_tema))
