#!/usr/bin/env python3

from django.urls import register_converter

from directorio.models import Organismo
from sistemas.models import Ente
from sistemas.models import Familia
from sistemas.models import Sistema
from sistemas.models import Tema
from sistemas.models import Usuario


class SistemaConverter:

    regex = '[0-9]+'

    def to_python(self, value) -> Sistema:
        sistema = Sistema.load_sistema(int(value))
        if not sistema:
            raise ValueError("El sistema especificado es incorrecto")
        return sistema

    def to_url(self, value) -> str:
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


class TemaConverter:

    regex = '[A-Za-z]{3}'

    def to_python(self, value):
        tema = Tema.load_tema(value)
        if not tema:
            raise ValueError("El tema especificado es incorrecto")
        return tema

    def to_url(self, value):
        if isinstance(value, str) and len(value) == 3:
            return value
        if isinstance(value, Tema):
            return str(value.id_tema)
        raise ValueError(
            "Se necesita una instancia de la clase Tema, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )


class EnteConverter:

    regex = '[A-Za-z][A-Za-z0-9_]+'

    def to_python(self, value):
        ente = Ente.load_ente(value)
        if not ente:
            raise ValueError("El ente especificado es incorrecto")
        return ente

    def to_url(self, value):
        if isinstance(value, str):
            return value
        if isinstance(value, Ente):
            return str(value.id_ente)
        raise ValueError(
            "Se necesita una instancia de la clase Ente, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )


class FamiliaConverter:

    regex = '[A-Za-z0-9_]{3}'

    def to_python(self, value):
        familia = Familia.load_familia(value)
        if not familia:
            raise ValueError("La familia especificada es incorrecta")
        return familia

    def to_url(self, value):
        if isinstance(value, str) and len(value) == 3:
            return value
        if isinstance(value, Familia):
            return str(value.id_familia)
        raise ValueError(
            "Se necesita una instancia de la clase Familia, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )


register_converter(FamiliaConverter, 'fam')
register_converter(OrganismoConverter, 'org')
register_converter(SistemaConverter, 'si')
register_converter(TemaConverter, 'tema')
register_converter(UserNameConverter, 'usr')
register_converter(EnteConverter, 'ent')
