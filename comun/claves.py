#!/usr/bin/env python3


import secrets


_SECRET_CODE_ALFABET = (
    '_-0123456789abcd'
    'efghijk[mnopqrst'
    'uvwxyzABCDEFGHIJ'
    'KLMN)PQRSTUVWXYZ'
    )


def generate_secret_token(length=20) -> str:
    """Genera un texto al azar, para usar como identificador de token
    o contraseña.

    Por defecto nos devuelve una cadena de texto de 20
    caracteres, seleccionados de un alfabeto de 64 posibles
    símbolos, lo que nos dá una entropía similar a la de
    UUID, pero es más corta y se puede usar sin modificar
    como parte de una URL.

    Parameters:

        - length (int): El número de caracteres que tendrá la
            contraseña o token. Por defecto 20 caracteres.

    Returns:

        (str) Una contraseña/token generada al azar.
    """
    return ''.join(
        secrets.choice(_SECRET_CODE_ALFABET)
        for _ in range(length)
        )


