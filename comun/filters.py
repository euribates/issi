#!/usr/bin/env python

import re
from urllib.parse import urlparse
from html import escape

"""
Estos filtros son funciones que esperan un único parámetro y devuelven
un único resultado. Están pensados sobre todo para limpiar o representar
datos en distintos formatos.

"""
def clean_text(text: str) -> str|None:
    """Limpia el formato de texto.

    - Si hay espacios al principio o al final se eliminan
    - Si tiene comillas dobles al principio y al final las elimina.
    - Si tiene comillas simples al principio y al final las elimina.
    - Si tiene triples comillas dobles al principio y al final las elimina.
    - Si tiene triples comillas simples al principio y al final las elimina.

    >>> assert clean_text('"hola"') == 'hola'

    Parameters:
        
        text (str): La cadena de texto a limpiar.

    Returns:

        Una cadena de texto limpia.
    """
    if text is None:
        return None
    text = text.strip()
    if text in {'', '_U'}:
        return None
        text = str(text)
    if len(text) > 5:
        if text[:3] == text[-3:] == '"""':
            return text[3:-3]
        if text[:3] == text[-3:] == "'''":
            return text[3:-3]
    if text[0] == text[-1] == '"':
        return text[1:-1]
    if text[0] == text[-1] == "'":
        return text[1:-1]
    return text


def clean_integer(text: str) -> int|None:
    """Interpreta una cadena de texto como un número entero.

    Los valores especiales ``''`` (cadena vacia) o ``'_U'`` se 
    interpretan como ``None``.

    >>> assert clean_integer('123') == 123
    >>> assert clean_integer('_U') is None

    Parameters:

        text (str): Una cadena de texto que contiene un número
                    entero, como ``'123'``.

    Returns:

        Un entero, o ``None``.
    """
    text = clean_text(text)
    if text is None:
        return text
    if not text.isdigit():
        raise ValueError(
            f"El valor indicado: {escape(text)}"
            " no parece un número entero."
            )
    return int(text) if text else None


def clean_url(url: str) -> str:
    """Limpia el formato de texto de una url.

    - Si ``url`` es nulo, vacio o el valor ``_U`` se devuelve ``None``
    - Verifica que empieza por ``http``
    - Realiza las mismas operaciones de limpieza que 
      :py:func:`clean_text`:

    >>> assert clean_url('http://www.python.org/') == 'http://www.python.org/'
    >>> assert clean_url(None) == None
    >>> assert clean_url('') == None
    >>> assert clean_url('_U') == None

    Params:
        
        - url (str): La cadena de texto con la URL a limpiar.

    Returns:

        Una cadena de texto con la URL limpia, o ``None``. Si la entrada
        no es vacia paro no tiene el formato de una URL se eleva la
        excepcion :py:exc:`ValueError`.
    """

    if url in {'_U', '', None}:
        return None
    url = clean_text(url)
    parts = urlparse(url)
    if parts.scheme not in {'http', 'https'}:
        raise ValueError(
            f"El valor indicado: {escape(url)}"
            " no parece tener el formato correcto."
            )
    return url


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
    """Transforma texto a un valor válido para usarse como *slug*.

    Sustituye espacios por el caracter ``'-'``, elimina caracteres
    especiales, convierte vocales acentuadas, reduce repeticiones,
    convierte mayúsculas a minúsculas y otras modificaciones que
    permiten usar el resultado como un valor seguro para ser usado como
    nombre de fichero, parte de la URL, etc.

    >>> slugify('Hola, mundo') == 'hola-mundo'

    Parameters:

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
