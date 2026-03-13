#!/usr/bin/env python3

import pandas as pd
from tempfile import TemporaryFile

from . import parsers


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
        result.insert(9, 'uuid', None)
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
            origin_names[9]: 'uuid',
            })
    else:
        raise ValueError(
            'Se esperaban 11 o 12 columnas, pero el fichero'
            f' tiene {len(origin_names)}'
            )
    return result


def pass_minimum(data: dict) -> bool:
    return all([
        data['codigo'].is_success(),
        data['nombre_sistema'].is_success(),
        ])


def list_all_errors(data):
    return [v for name, v in data.items() if v.is_failure()]


def importar_sistemas_desde_fichero(stream):
    with TemporaryFile() as fp:
        fp.write(stream)
        fp.seek(0)
        df = pd.read_excel(fp, engine="odf")
    df = rename_headers(df)
    for index, row in df.iterrows():
        data = parsers.parse_row(row, n_linea=index+1)
        yield (
            index,
            data, 
            pass_minimum(data),
            list_all_errors(data),
            )
