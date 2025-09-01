from typing import Optional

from django.db import models

JURISCAN_BASE = 'https://www3.gobiernodecanarias.org/juriscan'

class Rango(models.Model):
    id_rango = models.CharField(max_length=4, primary_key=True)
    nombre_rango = models.CharField(max_length=32, unique=True)
    peso = models.IntegerField()

    def __str__(self):
        return self.nombre_rango


class Norma(models.Model):
    id_norma = models.BigAutoField(primary_key=True)
    nombre_norma = models.TextField(max_length=620, unique=True)
    sobrenombre = models.CharField(max_length=32, blank=True)
    rango = models.ForeignKey(
        Rango,
        default='_na',
        related_name='normas',
        on_delete=models.PROTECT,
        )
    url = models.URLField(max_length=320, blank=True)
    id_juriscan = models.IntegerField(default=0)
    es_transversal = models.BooleanField(
        default=False,
        help_text=(
            "Este norma es aplicable a todos"
            " los sistemas de información."
            )
        )

    def __str__(self) -> str:
        if self.sobrenombre:
            return f'{self.sobrenombre} - {self.nombre_norma}'
        return self.nombre_norma

    def url_juriscan(self) -> Optional[str]:
        '''Devuelve la URL de la ficha de Juriscan, si existe, o None.
        '''
        if self.id_juriscan > 0:
            return f'{JURISCAN_BASE}/ficha.jsp?id={self.id_juriscan}'
        return None
