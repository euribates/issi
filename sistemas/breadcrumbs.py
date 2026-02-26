#!/usr/bin/env python3

from comun.breadcrumbs import APPS, BreadCrumb
from . import links
from . import models


def bc_issi() -> BreadCrumb:
    return APPS.step('ISSI', '/',)


def bc_sistemas() -> BreadCrumb:
    return bc_issi().step('bc_sistemas', links.a_sistemas())


def bc_alta_sistema() -> BreadCrumb:
    return bc_sistemas().step(
        'Alta sistema',
        links.a_alta_sistema(),
        )


def bc_detalle_sistema(sistema) -> BreadCrumb:
    return bc_sistemas().step(
        str(sistema.codigo),
        links.a_detalle_sistema(sistema.pk),
        )


def bc_cuestionario_sistema(sistema):
    return bc_detalle_sistema(sistema).step(
        'Cuestionario',
        links.a_cuestionario_sistema(sistema.pk),
        )


def bc_editar_sistema(sistema) -> BreadCrumb:
    return bc_sistemas().step(
        str(sistema.codigo),
        links.a_editar_sistema(sistema.pk),
        )


def bc_asignar_familia(sistema: models.Sistema) -> BreadCrumb:
    return bc_detalle_sistema(sistema).step(
        "Asignar familia",
        links.a_asignar_familia(sistema.pk),
        )


def bc_asignar_tema(sistema: models.Sistema) -> BreadCrumb:
    return bc_detalle_sistema(sistema).step(
        "Asignar bc_tema",
        links.a_asignar_tema(sistema.pk),
        )


def bc_editar_finalidad(sistema: models.Sistema) -> BreadCrumb:
    return bc_detalle_sistema(sistema).step(
        "Editar propósito",
        links.a_editar_finalidad(sistema.pk),
        )


def bc_editar_descripcion(sistema: models.Sistema) -> BreadCrumb:
    return bc_detalle_sistema(sistema).step(
        "Editar descripcion",
        links.a_editar_descripcion(sistema.pk),
        )


def bc_asignar_organismo(sistema: models.Sistema) -> BreadCrumb:
    return bc_detalle_sistema(sistema).step(
        "Asignar organismo",
        links.a_asignar_organismo(sistema.pk),
        )


def bc_asignar_icono(sistema: models.Sistema) -> BreadCrumb:
    return bc_detalle_sistema(sistema).step(
        "Asignar icono",
        links.a_asignar_icono(sistema.pk),
        )


def bc_asignar_responsable(sistema: models.Sistema) -> BreadCrumb:
    return bc_detalle_sistema(sistema).step(
        "Asignar responsable",
        links.a_asignar_responsable(sistema.pk),
        )


def bc_conmutar_campo(sistema: models.Sistema, field_name: str, verbose_name: str=''):
    if not verbose_name:
        verbose_name = field_name
    return bc_detalle_sistema(sistema).step(
        verbose_name,
        links.a_conmutar_campo(sistema.pk, field_name),
        )


def bc_usuarios() -> BreadCrumb:
    return bc_issi().step('bc_usuarios', links.a_usuarios())


def bc_alta_usuario() -> BreadCrumb:
    return bc_usuarios().step(
        'Alta',
        links.a_alta_usuario(),
        )


def bc_detalle_usuario(usuario: models.Usuario) -> BreadCrumb:
    return bc_usuarios().step(
        usuario.login,
        links.a_detalle_usuario(usuario.login),
        )


def bc_organismos() -> BreadCrumb:
    return bc_issi().step('bc_organismos', links.a_organismos())


def bc_entes() -> BreadCrumb:
    return bc_issi().step('bc_entes', links.a_entes())


def bc_detalle_ente(ente) -> BreadCrumb:
    return bc_entes().step(
        str(ente.id_ente),
        links.a_detalle_ente(ente.pk),
        )


def bc_asignar_interlocutor(ente) -> BreadCrumb:
    return bc_detalle_ente(ente).step(
        'Asignar interlocutor',
        links.a_asignar_interlocutor(ente.pk),
        )



def bc_detalle_organismo(organismo) -> BreadCrumb:
    return bc_organismos().step(
        organismo.nombre_organismo,
        links.a_detalle_organismo(organismo.pk),
        )


def bc_temas() -> BreadCrumb:
    return bc_issi().step('bc_temas', links.a_temas())


def bc_tema(t) -> BreadCrumb:
    return bc_temas().step(str(t), links.a_tema(t.id_tema))


def bc_familias() -> BreadCrumb:
    return bc_issi().step('bc_familias', links.a_familias())


def bc_detalle_familia(familia: models.Familia) -> BreadCrumb:
    return bc_familias().step(
        str(familia),
        links.a_detalle_familia(familia.pk),
        )


def bc_activos() -> BreadCrumb:
    return bc_sistemas().step('bc_activos', links.a_activos())


def bc_penientes() -> BreadCrumb:
    return bc_sistemas().step(
        'bc_penientes',
        links.a_pendientes(),
        )


def bc_sistemas_sin_tema() -> BreadCrumb:
    return bc_penientes().step(
        'Sin bc_tema asignado',
        links.a_sistemas_sin_tema(),
        )


def bc_exportar_sistemas() -> str:
    return bc_sistemas().step(
        'Exportar',
        links.a_exportar_sistemas(),
        )


def bc_importar_sistemas() -> str:
    return bc_sistemas().step(
        'Importar',
        links.a_importar_sistemas(),
        )


def bc_listado_preguntas():
    return bc_issi().step(
        'Cuestionario',
        links.a_listado_preguntas(),
        )


def bc_ver_pregunta(pregunta):
    return bc_listado_preguntas().step(
        f'Pregunta {pregunta.pk}',
        links.a_ver_pregunta(pregunta.pk),
        )

def bc_alta_opcion(pregunta):
    return bc_ver_pregunta(pregunta).step(
        'Añadir opción',
        links.a_alta_opcion(pregunta.pk),
        )
