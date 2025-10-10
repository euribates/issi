#!/usr/bin/env python3

from sistemas.models import Sistema
from sistemas.models import Usuario
from sistemas.models import Sistema
from directorio.models import Organismo


class SistemaConverter:

    regex = '[0-9]+'

    def to_python(self, value):
        sistema = Sistema.load_sistema(int(value))
        if not sistema:
            raise ValueError("El sistema especificado es incorrecto")
        return sistema

    def to_url(self, value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, Sistema):
            return str(value.id_sistema)
        raise ValueError(
            "Se necesita una instancia de la clase Sistema, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )


class UserNameConverter:

    regex = '[a-z][a-z0-9-.]+'

    def to_python(self, value):
        usuario = Usuario.load_usuario(value)
        if not usuario:
            raise ValueError("El usuario especificado es incorrecto")
        return usuario

    def to_url(self, value):
        if isinstance(value, str):
            return value
        if isinstance(value, Usuario):
            return str(value.login)
        raise ValueError(
            "Se necesita una instancia de la clase Usuario, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )


class SistemaConverter:

    regex = '[0-9]+'

    def to_python(self, value):
        sistema = Sistema.load_sistema(int(value))
        if not sistema:
            raise ValueError("El sistema especificado es incorrecto")
        return sistema

    def to_url(self, value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, Sistema):
            return str(value.id_sistema)
        raise ValueError(
            "Se necesita una instancia de la clase Sistema, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )



class OrganismoConverter:

    regex = '[0-9]+'

    def to_python(self, value):
        organismo = Organismo.load_organismo(int(value))
        if not organismo:
            raise ValueError("El organismo especificado es incorrecto")
        return organismo

    def to_url(self, value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, Organismo):
            return str(value.id_organismo)
        raise ValueError(
            "Se necesita una instancia de la clase Organismo, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )
