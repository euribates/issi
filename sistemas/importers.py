#!/usr/bin/env python3

from typing import Sequence, Callable
from tempfile import TemporaryFile

import pandas as pd

from comun.error import errors
from . import parsers
from . import models


def rename_headers(df):
    origin_names = list(df.columns)
    if len(origin_names) == 9:
        result = df.rename(columns={
            origin_names[0]: 'nombre_sistema',
            origin_names[1]: 'codigo',
            origin_names[2]: 'finalidad',
            origin_names[3]: 'materia',
            origin_names[4]: 'dir3',
            origin_names[5]: 'responsables_tecnologicos',
            origin_names[6]: 'responsables_funcionales',
            origin_names[7]: 'juriscan',
            origin_names[8]: 'comentarios',
            })
        result.insert(9, 'uuid_sistema', None)
    elif len(origin_names) == 10:
        result = df.rename(columns={
            origin_names[0]: 'nombre_sistema',
            origin_names[1]: 'codigo',
            origin_names[2]: 'finalidad',
            origin_names[3]: 'materia',
            origin_names[4]: 'dir3',
            origin_names[5]: 'responsables_tecnologicos',
            origin_names[6]: 'responsables_funcionales',
            origin_names[7]: 'juriscan',
            origin_names[8]: 'comentarios',
            origin_names[9]: 'uuid_sistema',
            })
    else:
        raise ValueError(
            'Se esperaban 9 o 10 columnas, pero el fichero'
            f' tiene {len(origin_names)}'
            )
    return result


def _necesita_actualizacion(sistema, payload) -> dict:
    result = dict()

    def chk(nombre):
        match nombre:
            case 'responsables_funcionales':
                old_value = {
                    persona.login
                    for persona in
                    sistema.get_responsables_funcionales()
                    }
                new_value = {
                    persona.login
                    for persona in 
                    payload.get('responsables_funcionales', [])
                    }
                if old_value != new_value:
                    result[nombre] = list(new_value)
            case 'responsables_tecnologicos':
                old_value = {
                    persona.login
                    for persona in
                    sistema.get_responsables_tecnologicos()
                    }
                new_value = {
                    persona.login
                    for persona in
                    payload.get('responsables_tecnologicos', [])
                    }
                if old_value != new_value:
                    result[nombre] = list(new_value)
            case 'juriscan':
                old_value = {j.id_juriscan for j in sistema.get_juriscan()}
                new_value = {j.pk for j in payload.get('juriscan', [])}
                if old_value != new_value:
                    result[nombre] = list(new_value)
            case _:
                old_value = getattr(sistema, nombre)
                new_value = payload[nombre]
                if old_value != new_value:
                    result[nombre] = new_value

    chk('nombre_sistema')
    chk('organismo')
    chk('codigo')
    chk('descripcion')
    chk('finalidad')
    chk('observaciones')
    chk('tema')
    chk('responsables_funcionales')
    chk('responsables_tecnologicos')
    chk('juriscan')
    return result


def _verificar_existencia_sistema(payload: dict) -> dict:
    '''Verifica si los datos a importar son consistentes con la BD.
    '''
    payload['necesita_actualizacion'] = True
    
    codigo = payload.get('codigo')
    if not codigo:
        return payload
    uuid_sistema = payload['uuid_sistema']
    # Si indica UUID, este debe existir en la base de datos
    if uuid_sistema:
        sistema = models.Sistema.load_sistema_por_uuid(uuid_sistema)
        if not sistema: 
            payload['errores'].append(errors.EI0010(uuid_sistema))
            return payload
        if sistema and sistema.codigo != codigo: 
            payload['errores'].append(errors.EI0014(
                uuid_sistema,
                payload_codigo=codigo,
                sistema_codigo=sistema.codigo,
                ))
            return payload
        payload['sistema_db'] = sistema
    else:
        sistema = models.Sistema.load_sistema_por_codigo(codigo)
        payload['sistema_db'] = sistema

    payload['necesita_actualizacion'] = True
    if sistema:
        delta = _necesita_actualizacion(sistema, payload)
        if delta:
            payload['delta'] = delta
        else:
            payload['necesita_actualizacion'] = False
    return payload


def importar_fila(items: Sequence, n_linea=None) -> dict:
    items = list(items)
    payload = {
        'errores': []
        }

    def chk(name: str, parser_fun: Callable, value: str, n_linea: int):
        result = parser_fun(value, n_linea=n_linea)
        if result.is_success():
            payload[name] = result.value
        else:
            payload['errores'].append(result.error_message)

    chk('nombre_sistema', parsers.parse_nombre_sistema, items[0], n_linea)
    chk('codigo', parsers.parse_codigo_interno, items[1], n_linea)
    chk('finalidad', parsers.parse_finalidad, items[2], n_linea)
    chk('descripcion', parsers.parse_descripcion, items[2], n_linea)
    chk('tema', parsers.parse_materia_competencial, items[3], n_linea)
    chk('organismo', parsers.parse_dir3, items[4], n_linea)
    chk('responsables_tecnologicos', parsers.parse_users, items[5], n_linea)
    chk('responsables_funcionales', parsers.parse_users, items[6], n_linea)
    chk('juriscan', parsers.parse_juriscan,items[7], n_linea)
    chk('observaciones', parsers.parse_observaciones, items[8], n_linea)
    chk('uuid_sistema', parsers.parse_uuid,items[9], n_linea)
    payload = _verificar_existencia_sistema(payload)
    return payload


def importar_sistemas_desde_fichero(stream):
    with TemporaryFile() as fp:
        fp.write(stream)
        fp.seek(0)
        df = pd.read_excel(fp, engine="odf")
    df = rename_headers(df)
    for _index, row in df.iterrows():
        payload = importar_fila(row, n_linea=_index + 1)
        if payload['errores'] or payload['necesita_actualizacion']:
            yield payload
