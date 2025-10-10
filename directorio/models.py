#!/usr/bin/env python3

from datetime import datetime as DateTime
from pathlib import Path
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

from django.db import models
from django.conf import settings

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

    def url_detalle_organismo(self) -> str:
        return links.a_detalle_organismo(self.pk)

    def url_organigrama(self):
        return links.a_organigrama(self.pk)

    def __str__(self):
        return self.nombre_organismo

    def calcula_ruta(self):
        self.ruta = f'{self.depende.ruta}{SEP}{self.depende_de.pk}'

    def es_primer_nivel(self) -> bool:
        return self.depende_de is None

    def iter_jerarquia(self, nivel=0):
        yield self, nivel
        for hijo in self.organismos_dependientes.all():
            yield from hijo.iter_jerarquia(nivel+1)


class Ente(models.Model):
    DATOS = 'datos.canarias.es'
    VALID_DAYS = 14

    id_ente = models.SlugField(
        max_length=12,
        primary_key=True,
        )
    organismo = models.OneToOneField(
        Organismo,
        related_name='ente',
        on_delete=models.PROTECT,
        )
    url_open_data = models.URLField(
        max_length=384,
        unique=True,
        blank=True,
        null=True,
        default=None,
        )

    @classmethod
    def load_ente(cls, pk:str):
        try:
            return cls.objects.get(id_ente=pk)
        except cls.DoesNotExist:
            return None

    def descargar_datos(self, url, force=False):
        slug = url.rsplit('/', 1)[1]
        filename = Path(f'{slug}.html')
        target_file = settings.BASE_DIR / Path(filename)
        if target_file.exists():
            stat = target_file.stat()
            mod_date = DateTime.fromtimestamp(stat.st_mtime)
            delta = DateTime.now() - mod_date
            is_still_valid = bool(delta.days <= self.VALID_DAYS)
            if is_still_valid and not force:  # El fichero local aun es válido
                return target_file
        urlretrieve(url, target_file)
        return target_file

    def get_open_data(self):
        url = self.url_open_data
        with open(self.descargar_datos(url), 'r', encoding='utf-8') as source:
            soup = BeautifulSoup(source, 'html.parser')
            for item in soup.find_all('li', 'dataset-item'):
                href = item.a.attrs['href']
                url = f'https://{self.DATOS}/{href}'
                desc = ''.join(item.a.contents)
                yield(url, desc)
