#!/usr/bin/env python3
# pylint: disable=no-member

from html import escape
import re
from uuid import UUID

from comun.funcop import static
from directorio.models import Organismo
from sistemas.models import Tema
from sistemas.models import Sistema
from sistemas.error import errors


DEFAULT_DOMAIN = 'gobiernodecanarias.org'

pat_username = re.compile(r"[a-zA-Z0-9_.+-]+$")
pat_email = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
pat_full = re.compile(r"(.+)\s+<(.+)>$")


@static(ya_vistos=set([]))
def parse_codigo_interno(codigo: str, n_linea=None):
    codigo = codigo.strip()
    if not codigo:
        raise errors.EI0003(n_linea=n_linea)
    pat_codigo_interno = re.compile(r'[A-Z_][0-9A-Z_][0-9A-Z_]+$')
    _match = pat_codigo_interno.match(codigo)
    if not _match:
        raise errors.EI0002(codigo, n_linea=n_linea)
    if codigo in parse_codigo_interno.ya_vistos:
        raise errors.EI0001(codigo, n_linea=n_linea)
    parse_codigo_interno.ya_vistos.add(codigo)
    return codigo


def parse_proposito(texto, n_linea) -> str:
    sublines = texto.splitlines()
    if len(sublines) > 0:
        return sublines[0]
    return ''


def parse_descripcion(text, n_linea) -> str:
    sublines = texto.splitlines()
    if len(sublines) > 1:
        return '\n\n'.join(sublines[1:])
    return ''


def parse_dir3(dir3, n_linea=None):
    dir3 = dir3.strip()
    if not dir3:
        return None
    organismo = Organismo.load_organismo_using_dir3(dir3)
    if not organismo:
        raise errors.EI0007(dir3, n_linea=n_linea)
    return organismo


def parse_materia_competencial(materia: str, n_linea=None) -> Tema|None:
    materia = materia.strip()
    if not materia:
        return Tema.load_tema('UNK')
    tema = Tema.load_tema(materia)
    if not tema:
        tema = Tema.load_tema_por_nombre(materia)
        if not tema:
            raise errors.EI0008(materia, n_linea=n_linea)
    return tema


def parse_users(txt: str, n_linea=None) -> set[dict]:
    result = []
    txt = txt.strip()
    if not txt:
        return result
    if ',' in txt:
        for item in pat_comma.split(txt):
            values = parse_users(item, n_linea=n_linea)
            if values:
                result.extend(values)
        return result
    match = pat_full.match(txt)
    if match:
        name = match.group(1)
        email = match.group(2)
        if pat_email.match(email):
            login = email.split('@', 1)[0]
            return [{
                'name': name,
                'login': login,
                'email': email,
    }]
    match = pat_email.match(txt)
    if match:
        login = txt.split('@', 1)[0]
        return [{
            'name': None,
            'login': login,
            'email': txt,
            }]
    match = pat_username.search(txt)
    if match:
        return [{
            'name': None,
            'login': txt,
            'email': f'{txt}@{DEFAULT_DOMAIN}'
            }]
    raise errors.EI0009(txt, n_linea=n_linea)


pat_integer = re.compile(r'\d+$')
pat_comma = re.compile(r'\s*,\s*')
pat_url_juriscan = re.compile(
    r'https?://www\d?\.gobiernodecanarias\.org/juriscan/ficha\.jsp\?id=(\d+)'
    )


def parse_juriscan(text: str|None, n_linea=None) -> list[int]:
    result = []
    if not bool(text):
        return result
    text = text.strip()
    match = pat_integer.match(text)
    if match:
        result.append(int(match.group(0)))
        return result
    if ',' in text:
        for item in pat_comma.split(text):
            values = parse_juriscan(item, n_linea=n_linea)
            if values:
                result.extend(values)
        return result
    for match in pat_url_juriscan.finditer(text):
        result.append(int(match.group(1)))
    return result


PAT_UUID = re.compile(r'[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


def parse_uuid(value: str, n_linea=None) -> UUID|None:
    if value is None:
        return None
    value = value.strip()
    if value == '':
        return None
    match = PAT_UUID.match(value)
    if match:
        return UUID(value)
    raise errors.EI0005(value)


CHECKS = [
    # (columna, field_name, parser_function),
    (0, 'nombre_sistema', None),
    (1, 'codigo', parse_codigo_interno),
    (2, 'proposito', parse_proposito),
    (2, 'descripcion', parse_descripcion),
    (3, 'tema', parse_materia_competencial),
    (4, 'organismo', parse_dir3),
    (5, 'responsables_tecnologicos', parse_users),
    (6, 'responsables_funcionales', parse_users),
    (7, 'juriscan', parse_juriscan),
    (9, 'comentarios', None),
    (10, 'uuid_sistema', parse_uuid),
    (

def parse_row(tupla, n_linea=None):
    n_cols = len(tupla)
    errors = []
    payload = {}
    for num_col, field_name, parser_function in CHECKS:
        try:
            value = tupla[num_col]
        except IndexError:
            value = None
        if parser_function:
            try:
                value = parser_function(value, n_linea=n_linea)
            except ValueError as err:
                errors.append(str(err))
        payload[field_name] = value
    

    if uuid_sistema:
            sistema = Sistema.load_sistema_por_uuid(uuid_sistema)
            if sistema:
                id_sistema = sistema.pk
    payload = {
        'id_sistema': id_sistema,
        'uuid': uuid_sistema,
        'nombre_sistema': nombre_sistema,
        'organismo': organismo,
        'codigo': codigo,
        'proposito': proposito,
        'descripcion': descripcion,
        'observaciones': comentarios,
        'tema': tema,
        'juriscan': juriscan,
        'responsables_tecnologicos': responsables_tecnologicos,
        'responsables_funcionales': responsables_funcionales,
        }
    return errors, payload
