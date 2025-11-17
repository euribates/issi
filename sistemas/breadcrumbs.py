#!/usr/bin/env python3

from comun.breadcrumbs import APPS, BreadCrumb
from . import links


def bc_issi() -> BreadCrumb:
    return APPS.step('ISSI', '/',)


def sistemas() -> BreadCrumb:
    return bc_issi().step('Sistemas', links.a_sistemas())


def alta_sistema() -> BreadCrumb:
    return sistemas().step(
        'Alta sistema',
        links.a_alta_sistema(),
        )


def detalle_sistema(sistema) -> BreadCrumb:
    return sistemas().step(
        str(sistema.codigo),
        links.a_detalle_sistema(sistema.pk),
        )


def editar_sistema(sistema) -> BreadCrumb:
    return sistemas().step(
        str(sistema.codigo),
        links.a_editar_sistema(sistema.pk),
        )


def asignar_tema(sistema) -> BreadCrumb:
    return detalle_sistema(sistema).step(
        "Asignar tema",
        links.a_asignar_tema(sistema.pk),
        )


def editar_proposito(sistema) -> BreadCrumb:
    return detalle_sistema(sistema).step(
        "Editar propósito",
        links.a_editar_proposito(sistema.pk),
        )


def editar_descripcion(sistema) -> BreadCrumb:
    return detalle_sistema(sistema).step(
        "Editar descripcion",
        links.a_editar_descripcion(sistema.pk),
        )


def asignar_organismo(sistema) -> BreadCrumb:
    return detalle_sistema(sistema).step(
        "Asignar organismo",
        links.a_asignar_organismo(sistema.pk),
        )


def asignar_icono(sistema) -> BreadCrumb:
    return detalle_sistema(sistema).step(
        "Asignar icono",
        links.a_asignar_icono(sistema.pk),
        )


def asignar_responsable(sistema) -> BreadCrumb:
    return detalle_sistema(sistema).step(
        "Asignar responsable",
        links.a_asignar_responsable(sistema.pk),
        )

def conmutar_campo(sistema, field_name, verbose_name=''):
    if not verbose_name:
        verbose_name = field_name
    return detalle_sistema(sistema).step(
        verbose_name,
        links.a_conmutar_campo(sistema.pk, field_name),
        )

def usuarios() -> BreadCrumb:
    return bc_issi().step('Usuarios', links.a_usuarios())


def detalle_usuario(usuario) -> BreadCrumb:
    return usuarios().step(
        usuario.login,
        links.a_detalle_usuario(usuario.login),
        )


def organismos() -> BreadCrumb:
    return bc_issi().step('Organismos', links.a_organismos())


def entes() -> BreadCrumb:
    return bc_issi().step('Entes', links.a_entes())


def detalle_ente(ente) -> BreadCrumb:
    return entes().step(
        str(ente.id_ente),
        links.a_detalle_ente(ente.pk),
        )

def detalle_organismo(organismo) -> BreadCrumb:
    return organismos().step(
        organismo.nombre_organismo,
        links.a_detalle_organismo(organismo.pk),
        )


def temas() -> BreadCrumb:
    return bc_issi().step('Temas', links.a_temas())


def tema(t) -> BreadCrumb:
    return temas().step(str(t), links.a_tema(t.id_tema))


def activos() -> BreadCrumb:
    return sistemas().step('Activos', links.a_activos())


def pendientes() -> BreadCrumb:
    return sistemas().step(
        'Pendientes',
        links.a_pendientes(),
        )


def sistemas_sin_tema() -> BreadCrumb:
    return pendientes().step(
        'Sin tema asignado',
        links.a_sistemas_sin_tema(),
        )
