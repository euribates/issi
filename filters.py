#!/usr/bin/env python

import re

from typing import Optional

def clean_text(text: str) -> str:
    """Limpia el formato de texto.

    - Si hay espacios al principio o al final se eliminan
    - Si tiene comillas dobles al principio y al final las elimina.
    - Si tiene comillas simples al principio y al final las elimina.

    >>> assert clean_text('"hola"') == 'hola'

    Params:
        
        - text (str): La cadena de texto a limpiar.

    Returns:

        Una cadena de texto limpia.
    """
    text = text.strip()
    if text[0] == text[-1] == '"':
        return text[1:-1]
    if text[0] == text[-1] == "'":
        return text[1:-1]
    return text


def clean_integer(text: str) -> Optional[int]:
    """Interpreta una cadena de texto como un número entero.

    Los valores especiales '' (cadena vacia) o `'_U'` se 
    interpretan como `None`.

    >>> assert clean_integer('123') == 123
    >>> assert clean_integer('_U') is None

    Params:

        text (str): Una cadena de texto que contiene un número
                    entero, como `'123'`.

    Returns:

        Un entero, o `None`.
    """
    if text in {'_U', '', None}:
        return None
    return int(text)


_SLUGIFY_MAP = {
    32: 45,  # space -> hyphen
    33: None,  # exclamation mark
    34: None,  # double quotes
    35: None,  # hash
    36: None,  # dollar
    37: None,  # percent
    38: None,  # ampersand
    39: None,  # simple quote
    40: None,  # open par
    41: None,  # close par
    42: None,  # asterisk
    43: 45,  # plus -> hyphen
    44: None,  # comma
    46: None,  # dot or full stop
    47: 45,  # slash -> hyphen
    58: 45,  # colon -> hyphen
    59: 45,  # semicolon -> hyphen
    60: None,  # open angled bracket
    61: 45,  # equals -> hyphen
    62: None,  # close angled bracket
    63: None,  # question mark
    64: 45,  # @ -> hyphen
    91: None,  # open bracket
    92: 45,  # backslash -> hyphen
    93: None,  # close bracket
    94: 45,  # caret -> hyphen
    95: 45,  # underscore -> hyphen
    96: None,  # grave accent
    123: None,  # open brace
    124: 45,  # pipe -> hyphen
    125: None,  # close brace
    126: 45,  # equivalency sign (~) -> hyphen
    133: 45,  # ellipsis
    191: None,  # open question mark
    193: 65,
    201: 69,
    205: 73,
    209: 78,
    211: 79,
    218: 85,
    220: 85,
    225: 97,  # a
    233: 101,
    237: 105,
    241: 110,
    243: 111,
    250: 117,
    252: 117,
    8230: 45,  # ellipsis
}

_SLUGIFY_PAT_MULTIPLE_HYPHENS = re.compile(r'--+')


def slugify(texto: str) -> str:
    """Transforma texto a un valor válido para usarse como _slug_

    Sustituye espacion por el caracter `'-'`, elimina caracteres
    especiales, convierte vocales acentuadas, reduce repeticiones,
    convierte mayúsculas a minúsculas y otras modificaciones que
    permiten usar el resultado como un valor seguro para ser usado como
    nombre de fichero, parte de la URL, etc.

    >>> slugify('Hola, mundo') == 'hola-mundo'

    Params:

        text (str): El texto a transformar

    Returns:

        Una cadena de texto apta para ser usada como nombre de un fichero,
        parte de una URL, etc. 
    """
    result = texto.lower()
    result = result.replace('ñ', 'nn')
    result = result.replace('€', '-euros')
    result = result.translate(_SLUGIFY_MAP)
    result = ''.join([_ for _ in result if ord(_) < 129])
    result = _SLUGIFY_PAT_MULTIPLE_HYPHENS.sub('-', result)
    return result


def clean_url(url: str) -> str:
    """Limpia el formato de texto de una url.

    - Si `url` es nulo, vacio o el valor `_U` se devuelve None
    - Verifica que empieza por http
    - Realiza las mismas operaciones de limpieza que `clean_text`:
        - Si hay espacios al principio o al final se eliminan
        - Si tiene comillas dobles al principio y al final las elimina.
        - Si tiene comillas simples al principio y al final las elimina.

    >>> assert clean_url('http://www.python.org/') == 'http://www.python.org/'
    >>> assert clean_url(None) == None
    >>> assert clean_url('') == None
    >>> assert clean_url('_U') == None

    Params:
        
        - url (str): La cadena de texto con la URL a limpiar.

    Returns:

        Una cadena de texto con la URL limpia, o `None`.
    """

    if url in {'_U', '', None}:
        return None
    url = clean_text(url)
    assert url.startswith('http')
    return url

