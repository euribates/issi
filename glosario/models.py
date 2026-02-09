#!/usr/bin/env python

from django.db import models


class Termino(models.Model):
    """Modelo de entrada en el glosario.

    Conta de un identificador del término, el término en si, la
    descripción y, en el caso de que la hubiera, una URL de referencia,
    opcional.

    .. graphviz:: images/glosario.dot
    """

    class Meta:
        ordering = ['entrada',]

    id_termino = models.BigAutoField(primary_key=True)
    entrada = models.CharField(unique=True, max_length=128)
    descripcion = models.TextField(max_length=1024)
    fuente = models.URLField(max_length=512, blank=True, default='')

    def __str__(self):
        return self.entrada


class Fuente(models.Model):
    """Modelo de Fuentes normativas.

    Ordenadas por el principio de jerarquía normativa

    - Derecho comunitario
        - Reglamento europeo (Aplicable direcetamente)
        - Directiva (Requiere transposición)
        - Decisión
        - Recomendaciones y dictámenes (No vinculantes)
    - Constitución Española
    
    - Tratados internacionales

    - Leyes

        - Ley orgánica       ┐
        - Ley ordinaria      ├ Al mismo nivel
        - Leyes autonómicas  ┘

    - Decretos

        - Real Decreto Legislativo ┐
                                   ├ Rango de ley
        - Real Decreto Ley         ┘
    
    - Reglamento

       - Aprobadas por Real Decreto del Presidente del Gobierno
         o acordado en el consejo de ministros.

       - Aprobadas por orden ministerial.

    - Costumbre.
    - Principios generales de derecho.
    """

    class Meta:
        ordering = ['alias',]

    id_fuente = models.BigAutoField(primary_key=True)
    alias = models.CharField(max_length=32, unique=True)
    descripcion = models.TextField(max_length=512, unique=True)
    url = models.URLField(max_length=256, blank=True)

    def __str__(self):
        if self.alias:
            return f'{self.alias} - {self.descripcion}'
        return self.descripcion
