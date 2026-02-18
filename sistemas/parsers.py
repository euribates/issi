#!/usr/bin/env python3
# pylint: disable=no-member

"""
Todas las funciones definidas en este módulo
deben devolver o bien un pbjeto de la clase
``Success`` o uno de la clase ``Failure``.

El valor devuelto dentro de ``Success`` deberia
ser del tipo más cercanbo posible al esperado.
"""

import re
from uuid import UUID
from typing import Sequence

import pandas as pd

from caches.temas import temas
from comun.funcop import first
from comun.results import Result, Success, Failure
from comun.error import errors
from directorio.models import Organismo
from juriscan.models import Juriscan
from sistemas.models import Tema
from sistemas.models import Usuario

#: Dominio por defecto para los correos electrónicos.
DEFAULT_DOMAIN = 'gobiernodecanarias.org'

#: Patron para localizar separados coma y punto y coma
pat_sep = re.compile(r'\s*[,;]\s*')

#: Patrón para detectar valores de username
pat_username = re.compile(r"^[a-zA-Z0-9_.+-]+$")

#: Patrón para detectar correos electrónicos simples
pat_email = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

#: Patrón para detectar correos elctrónicos completos
pat_full = re.compile(r"(.+)\s+<(.+@.+)>$")

#: Patrón para detectar números enteros
pat_integer = re.compile(r'\d+$')

#: Patron para detectar enlaces a Juriscán
pat_url_juriscan = re.compile(
    r'https?://www\d?\.gobiernodecanarias\.org/juriscan/ficha\.jsp\?id=(\d+)'
    )

#: Patron para detectar UUID
pat_uuid = re.compile(r'[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


def parse_nombre_sistema(texto: str, n_linea=None) -> Result:
    """Parsea el nombre del sistema.

    Este no puede ser nulo, y debe tener como mínimo tres
    caracteres. Si hay un punto al final, se elimina.

    Ejemplo de uso:

        >>> rs = parse_nombre_del_sistema('')
        >>> assert rs.is_failure()
        >>> rs = parse_nombre_del_sistema('Ares.')
        >>> assert rs.is_success()
        >>> assert rs.value = 'Ares'

    Parameters:

        - texto (str): El texto que contiene el nombre del sistema.

    Returns:

        (Result) ``Success`` si el nombre se considera válido,
          ``Failure`` en caso contrario.

    """
    if texto:
        texto = texto.strip()
        if texto[-1] == '.':
            texto = texto[:-1]
        if len(texto) > 3:
            return Success(texto)
    return Failure(errors.EI0013(texto, n_linea=n_linea))


def parse_codigo_interno(codigo: str, n_linea=None) -> Result:
    '''devuelve el código identificativo interno (CII) del sistema.
    '''
    if codigo is None or pd.isna(codigo):
        return Failure(errors.EI0003(n_linea=n_linea))
    codigo = codigo.strip()
    if not codigo:
        return Failure(errors.EI0003(n_linea=n_linea))
    pat_codigo_interno = re.compile(r'[A-Z_][0-9A-Z_][0-9A-Z_]+$')
    _match = pat_codigo_interno.match(codigo)
    if not _match:
        return Failure(errors.EI0002(codigo, n_linea=n_linea))
    return Success(codigo)


def parse_finalidad(texto, n_linea=None) -> Result:
    if texto is None or pd.isna(texto):
        return Success('')
    texto = texto.strip()
    sublines = texto.splitlines()
    if len(sublines) > 0:
        return Success(sublines[0])
    else:
        return Success(texto)


def parse_descripcion(texto, n_linea=None) -> Result:
    if texto is None or pd.isna(texto):
        return Success('')
    sublines = texto.splitlines()
    if len(sublines) > 1:
        return Success('\n\n'.join(sublines[1:]))
    return Success('')


def parse_comentarios(texto, n_linea=None) -> Result:
    if texto is None or pd.isna(texto):
        return Success('')
    texto = texto.strip()
    if texto == '':
        return Success('')
    sublines = texto.splitlines()
    return Success('\n\n'.join(sublines))


def parse_dir3(dir3, n_linea=None) -> Result:
    if dir3 is None:
        return Success(None)
    dir3 = str(dir3).strip()
    if not dir3:
        return Success(None)
    organismo = Organismo.load_organismo_using_dir3(dir3)
    if organismo:
        return Success(organismo)
    return Failure(errors.EI0007(dir3, n_linea=n_linea))


def parse_materia_competencial(materia: str | None, n_linea=None) -> Result:
    '''Devuelve la materia competencial que corresponda.

    Si no se especifica, devuelve la materia ``UNK``.
    '''
    if materia is None:
        return Success(Tema.load_tema('UNK'))
    materia = materia.strip()
    if materia == '':
        return Success(Tema.load_tema('UNK'))
    if materia in temas:
        return Success(Tema.load_tema(materia))
    for codigo, descripcion in temas.items():
        if descripcion == materia:
            return Success(Tema.load_tema(codigo))
    return Failure(errors.EI0008(materia, n_linea=n_linea))


def _parse_one_user(text: str, n_linea: int) -> Success|Failure:
    if match := pat_full.match(text):
        nombre = match.group(1)
        email = match.group(2)
        username = first(email.split('@'))
    elif match := pat_email.match(text):
        username = first(text.split('@'))
        email = text
        nombre = None
    elif match := pat_username.search(text):
        username = text
        email = f'{text}@{DEFAULT_DOMAIN}'
        nombre = None
    else:
        return Failure(errors.EI0009(text, n_linea=n_linea))
    usuario = Usuario.load_usuario_by_username(username) or Usuario(
            login=username,
            email=email,
            nombre=nombre,
            )
    return Success(usuario)


def parse_users(text: str, n_linea=None) -> Result:
    """Devuelve un conjunto de usuarios.
    """
    if not text or pd.isna(text):
        return Success(set())
    text = text.strip()
    if '\n' in text:
        items = list(text.splitlines(text))
    elif ',' in text or ';' in text:
        items = list(pat_sep.split(text))
    else:
        items = [text]
    result = set()
    for item in items:
        user = _parse_one_user(item, n_linea=n_linea)
        if user.is_failure():
            return Failure(errors.EI0009(item))
        result.add(user.value)
    return Success(result)


def _parse_one_juriscan(text: str, n_linea=None) -> Result:
    if match := pat_integer.match(text):
        id_juriscan = int(match.group(0))
        juriscan = Juriscan.load_or_create(id_juriscan)
        if juriscan is not None:
            return Success(juriscan)
    if match := pat_url_juriscan.match(text):
        id_juriscan = int(match.group(1))
        juriscan = Juriscan.load_or_create(id_juriscan)
        if juriscan is not None:
            return Success(juriscan)
    return Failure(errors.EI0012(text))


def parse_juriscan(text: str|None, n_linea=None) -> Result|Failure:
    if not text or pd.isna(text):
        return Success(set())
    text = str(text).strip()
    if '\n' in text:
        items = list(text.splitlines(text))
    elif ',' in text or ';' in text:
        items = list(pat_sep.split(text))
    else:
        items = [text]
    result = set()
    for item in items:
        ficha = _parse_one_juriscan(item, n_linea=n_linea)
        if ficha.is_failure():
            return Failure(errors.EI0012(item))
        result.add(ficha.value)
    return Success(result)


def parse_uuid(value: str, n_linea=None) -> Result:
    if not value or pd.isna(value):
        return Success(None)
    if value:
        value = value.strip()
        match = pat_uuid.match(value)
        if match:
            return Success(UUID(value))
    return Failure(errors.EI0005(value))



def parse_row(tupla: Sequence, n_linea=None) -> dict:
    result = {}
    result['nombre_sistema'] = parse_nombre_sistema(tupla[0], n_linea=n_linea)
    result['codigo'] = parse_codigo_interno(tupla[1], n_linea=n_linea)
    result['finalidad'] = parse_finalidad(tupla[2], n_linea=n_linea)
    result['descripcion'] = parse_descripcion(tupla[2], n_linea=n_linea)
    result['tema'] = parse_materia_competencial(tupla[3], n_linea=n_linea)
    result['organismo'] = parse_dir3(tupla[4], n_linea=n_linea)
    result['responsables_tecnologicos'] = parse_users(tupla[5], n_linea=n_linea)
    result['responsables_funcionales'] = parse_users(tupla[6], n_linea=n_linea)
    result['juriscan'] = parse_juriscan(tupla[7], n_linea=n_linea)
    result['comentarios'] = parse_comentarios(tupla[8], n_linea=n_linea)
    result['uuid'] = parse_uuid(tupla[9], n_linea=n_linea)
    return result
