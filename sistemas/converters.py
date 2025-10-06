#!/usr/bin/env python3

from . import models


class SistemaConverter:

    regex = '[0-9]+'

    def to_python(self, value):
        sistema = models.Sistema.load_sistema(int(value))
        if not sistema:
            raise ValueError("El sistema especificado es incorrecto")
        return sistema

    def to_url(self, value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, models.Sistema):
            return str(value.id_sistema)
        raise ValueError(
            "Se necesita una instancia de la clase Sistema, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )


class UserNameConverter:

    regex = '[a-z][a-z0-9-]+'

    def to_python(self, value):
        usuario = models.Usuario.load_usuario(value)
        if not usuario:
            raise ValueError("El usuario especificado es incorrecto")
        return usuario

    def to_url(self, value):
        if isinstance(value, str):
            return value
        if isinstance(value, models.Usuario):
            return str(value.login)
        raise ValueError(
            "Se necesita una instancia de la clase Usuario, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )


class SistemaConverter:

    regex = '[0-9]+'

    def to_python(self, value):
        sistema = models.Sistema.load_sistema(int(value))
        if not sistema:
            raise ValueError("El sistema especificado es incorrecto")
        return sistema

    def to_url(self, value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, models.Sistema):
            return str(value.id_sistema)
        raise ValueError(
            "Se necesita una instancia de la clase Sistema, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )
