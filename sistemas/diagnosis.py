#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class DiagnosticoSistema:
    tiene_proposito: bool
    tiene_descripcion: bool
    tiene_organismo: bool
    tiene_tema: bool
    tiene_algun_responsable: bool

    def __init__(self, sistema):
        self._sistema = sistema
        self.evaluate()

    def evaluate(self):
        self.tiene_proposito = bool(self._sistema.proposito)
        self.tiene_organismo = bool(self._sistema.organismo)
        self.tiene_descripcion = bool(self._sistema.descripcion)
        self.tiene_tema = bool(self._sistema.tema.pk != 'UNK')
        self.tiene_algun_responsable = self._sistema.perfiles.count() > 0

    def flags(self) -> list[bool]:
        return [
            self.tiene_proposito,
            self.tiene_descripcion,
            self.tiene_organismo,
            self.tiene_tema,
            self.tiene_algun_responsable,
            ]

    def evaluaciones(self) -> list[str]:
        self.evaluate()
        result = []
        if not self.tiene_proposito:
            result.append('No se ha definido el campo propósito')
        if not self.tiene_descripcion:
            result.append('No se ha definido el campo descripción')
        if not self.tiene_organismo:
            result.append(
                'No se ha asignado el sistema'
                ' a ningún puesto del organigrama'
                )
        if not self.tiene_tema:
            result.append('Pendiente de asignar tema')
        if not self.tiene_algun_responsable:
            result.append('No se ha definido ningún responsable para este sistema')
        return result

    def __bool__(self) -> bool:
        return any(self.flags())
