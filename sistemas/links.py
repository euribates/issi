#!/usr/bin/env python3

"""
Fichero para la creación de enlaces.

Todas las funciones públicas en este fichero deberían empezar por a_. Deden
devolver una string con la url relativa tal y como estén definidas 
en el fichero `urls.py`.

La función privada _a es una ayuda para escribir las funciones.

"""

from django.urls import reverse_lazy


def _a(name: str, **kwargs) -> str:
    '''Azucar sintactico para definir funciones a_*.
    '''
    return str(reverse_lazy(name, kwargs=kwargs))


def a_sistemas() -> str:
    return _a('sistemas:index')


def a_alta_sistema() -> str:
    return _a('sistemas:alta_sistema')


def a_detalle_sistema(id_sistema: int) -> str:
    return _a('sistemas:detalle_sistema', sistema=id_sistema)


def a_editar_sistema(id_sistema: int) -> str:
    return _a('sistemas:editar_sistema', sistema=id_sistema)


def a_asignar_familia(id_sistema: int) -> str:
    return _a('sistemas:asignar_familia', sistema=id_sistema)


def a_asignar_tema(id_sistema: int) -> str:
    return _a('sistemas:asignar_tema', sistema=id_sistema)


def a_asignar_icono(id_sistema: int) -> str:
    return _a('sistemas:asignar_icono', sistema=id_sistema)


def a_editar_proposito(id_sistema: int) -> str:
    return _a('sistemas:editar_proposito', sistema=id_sistema)


def a_editar_descripcion(id_sistema: int) -> str:
    return _a('sistemas:editar_descripcion', sistema=id_sistema)


def a_asignar_organismo(id_sistema: int) -> str:
    return _a('sistemas:asignar_organismo', sistema=id_sistema)


def a_asignar_responsable(id_sistema: int) -> str:
    return _a('sistemas:asignar_responsable', sistema=id_sistema)


def a_conmutar_campo(id_sistema: int, campo: str) -> str:
    return _a('sistemas:conmutar_campo',
        sistema=id_sistema,
        campo=campo,
        )


def a_usuarios() -> str:
    return _a('sistemas:listado_usuarios')


def a_alta_usuario() -> str:
    return _a('sistemas:alta_usuario')


def a_detalle_usuario(usuario) -> str:
    return _a('sistemas:detalle_usuario', usuario=usuario)


def a_organismos() -> str:
    return _a('sistemas:listado_organismos')
    

def a_entes() -> str:
    return _a('sistemas:listado_entes')
    

def a_detalle_ente(id_ente) -> str:
    return _a('sistemas:detalle_ente', ente=id_ente)


def a_asignar_interlocutor(id_ente) -> str:
    return _a('sistemas:asignar_interlocutor', ente=id_ente)


def a_detalle_organismo(id_organismo) -> str:
    return _a('sistemas:detalle_organismo', organismo=id_organismo)


def a_temas() -> str:
    return _a('sistemas:listado_temas')


def a_tema(id_tema:str) -> str:
    return _a('sistemas:detalle_tema', tema=id_tema)


def a_familias() -> str:
    return _a('sistemas:listado_familias')


def a_detalle_familia(familia: str) -> str:
    return _a('sistemas:detalle_familia', familia=familia)


def a_activos() -> str:
    return _a('sistemas:listado_activos')


def a_pendientes() -> str:
    return _a('sistemas:pendientes')


def a_sistemas_sin_tema() -> str:
    return _a('sistemas:sistemas_sin_tema')


def a_importar_sistemas() -> str:
    return _a('sistemas:importar_sistemas')


def a_exportar_sistemas() -> str:
    return _a('sistemas:exportar_sistemas')


def a_importar_sistemas() -> str:
    return _a('sistemas:importar_sistemas')
