#!/usr/bin/env python3

from . import models


class OrganismoConverter:

    regex = '[0-9]+'

    def to_python(self, value):
        organismo = models.Organismo.load_organismo(int(value))
        if not organismo:
            raise ValueError("El organismo especificado es incorrecto")
        return organismo

    def to_url(self, value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, models.Organismo):
            return str(value.id_organismo)
        raise ValueError(
            "Se necesita una instancia de la clase Organismo, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )
