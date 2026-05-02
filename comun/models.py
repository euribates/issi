#!/usr/bin/env python3

import random
from datetime import timedelta as TimeDelta

from django.db import models
from django.utils import timezone

TOKEN_VALID_DAYS = 3

SECRET_CODE_ALFABET = (
    '_-0123456789abcd'
    'efghijk[mnopqrst'
    'uvwxyzABCDEFGHIJ'
    'KLMN)PQRSTUVWXYZ'
    )


def generate_secret_code(length=20) -> str:
    """Genera un texto al azar, como identificador del token.

    Por defecto nos devuelve una cadena de texto de 20 
    caracteres, seleccionados de un alfabeto de 64 posibles
    símbolos, lo que nos dá una entropía similar a la de
    UUID, pero es más corta y se puede usar sin modificar
    como parte de una URL.
    """
    return ''.join(
        random.choice(SECRET_CODE_ALFABET)
        for _ in range(length)
        )


class EmailToken(models.Model):

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'tokens'
        ordering = ['created_at']

    token = models.CharField(
        max_length=20,
        default=generate_secret_code,
        primary_key=True,
        )
    email = models.EmailField(
        max_length=350,
        )
    created_at = models.DateTimeField(
        default=timezone.now,
        )
    valid_for = models.DurationField(
        default=TimeDelta(days=TOKEN_VALID_DAYS),
        )

    def __str__(self) -> str:
        return f'{self.token[:4]}************{self.token[-4:]}'

    @classmethod
    def load_token(cls, pk: str):
        """Obtener un token a partir de su clave primaria.

        Parameters:

            pk (int): Clave primaria del sistema

        Returns:

            La instancia, si existe el registro correspondiente
            en la base de datos, o ``None`` en caso contrario.
        """
        try:
            return cls.objects.get(token=pk)
        except cls.DoesNotExist:
            return None
