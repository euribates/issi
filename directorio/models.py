#!/usr/bin/env python3

from django.db import models
from django.db.models import Q
from django.utils import timezone

from . import links




class Organismo(models.Model):

    class Meta:
        ordering = ['nombre_organismo']

    id_organismo = models.BigIntegerField(primary_key=True)
    nombre_organismo = models.CharField(
        max_length=144,
        unique=True,
        )
    dir3 = models.CharField(max_length=9, unique=True)
    id_sirhus = models.IntegerField(unique=True)
    categoria = models.CharField(max_length=40)
    competencias = models.TextField(
        blank=True,
        null=True,
        default=None,
        )
    depende_de = models.ForeignKey(
        'Organismo',
        related_name='organismos_dependientes',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        )
    ruta = models.CharField(
        max_length=128,
        default='',
        )
    url = models.URLField(
        max_length=384,
        blank=True,
        null=True,
        default=None,
        )
    f_alta = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha en la que el organismo se dio de alta",
        )
    f_cambio = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de la última modificación del organismo",
        )
    f_baja = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        )

    @classmethod
    def load_organismo(cls, pk:int):
        try:
            return cls.objects.get(id_organismo=pk)
        except cls.DoesNotExist:
            return None

    @classmethod
    def load_organismo_using_dir3(cls, dir3: str):
        try:
            return cls.objects.get(dir3=dir3)
        except cls.DoesNotExist:
            return None

    @classmethod
    def upsert(cls, id_organismo, **kwargs):
         organismo, created = cls.objects.update_or_create(
            pk=id_organismo,
            defaults=kwargs,
            )
         return organismo, created

    @classmethod
    def needs_update(cls, id_organismo: int, payload: dict) -> bool:
        '''Devuelve verdadero si la instancia necesita ser actualizada.
        '''
        org = cls.load_organismo(id_organismo)
        if org is None:
            return True
        for name in payload:
            new_value = payload[name]
            old_value = getattr(org, name)
            if  new_value != old_value:
                return True
        return False

    @classmethod
    def search_organismos(cls, query):
        return (
            cls.objects.filter(
                Q(nombre_organismo__icontains=query) |
                Q(categoria__icontains=query) |
                Q(dir3__icontains=query)
                )
            )

    def url_detalle_organismo(self) -> str:
        return links.a_detalle_organismo(self.pk)

    def url_organigrama(self):
        return links.a_organigrama(self.pk)

    def __str__(self):
        return self.nombre_organismo

    def calcula_ruta(self, sep='/'):
        self.ruta = f'{self.depende.ruta}{sep}{self.depende_de.pk}'

    def es_primer_nivel(self) -> bool:
        if self.depende_de is None:
            return True
        return self.depende_de.pk == 1

    def iter_jerarquia(self, nivel=0):
        yield self, nivel
        for hijo in self.organismos_dependientes.all():
            yield from hijo.iter_jerarquia(nivel+1)

    def touch(self):
        '''Marcar el sistema como modificado.

        Todos los sistemas jerarquicamenete superiores
        son marcados también como modificados.
        '''
        self.f_cambio = timezone.now()
        self.save(update_fields=['f_cambio'])
        if self.depende_de.exists():
            self.depende_de.touch()
