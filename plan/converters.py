#!/usr/bin/env python3

from . import models


class TareaConverter:

    regex = '[0-9]+'

    def to_python(self, value) -> models.Backlog:
        tarea = models.Backlog.load_backlog(int(value))
        if not tarea:
            raise ValueError(
                "La tarea de backlog especificada"
                " es incorrecta"
                )
        return tarea

    def to_url(self, value) -> str:
        if isinstance(value, int):
            return str(value)
        if isinstance(value, models.Backlog):
            return str(value.id_backlog)
        raise ValueError(
            "Se necesita una instancia de la clase Backlog, pero"
            " me pasan una instancia de {value.__class__.__name__}."
            )
