#!/usr/bin/env python

from django.db import models


class Termino(models.Model):

    class Meta:
        ordering = ['entrada',]

    id_termino = models.BigAutoField(primary_key=True)
    entrada = models.CharField(unique=True, max_length=128)
    descripcion = models.TextField(max_length=1024)
    fuente = models.CharField(max_length=512, blank=True, default='')

    def __str__(self):
        return self.entrada


class Fuente(models.Model):

    class Meta:
        ordering = ['alias',]

    id_fuente = models.BigAutoField(primary_key=True)
    alias = models.CharField(max_length=32, unique=True)
    descripcion = models.TextField(max_length=512, unique=True)
    url = models.URLField(max_length=256, blank=True)
