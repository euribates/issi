#!/usr/bin/env python3

from sistemas.models import Sistema
from sistemas.models import Usuario
from sistemas.models import Sistema
from sistemas.models import Tema
from sistemas.models import Perfil
from directorio.models import Organismo
from directorio.models import Ente


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


class PerfilConverter:

    regex = '[0-9]+'

    def __init__(self, *args, **kwargs):
        from icecream import ic; ic()
        super().__init__(*args, **kwargs)


    def to_python(self, value):
        from icecream import ic; ic()
        perfil = Perfil.load_perfil(int(value))
        if not perfil:
            raise ValueError("El perfil especificado es incorrecto")
        return perfil

    def to_url(self, value):
        from icecream import ic; ic()
        if isinstance(value, int):
            return str(value)
        if isinstance(value, Perfil):
            return str(value.id_perfil)
        raise ValueError(
            "Se necesita una instancia de la clase Perfil, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )


