#!/usr/bin/env python3

"""
Modelos definidos para intermediar con Juriscan.
"""


from urllib.request import urlopen
from django.utils import timezone

from bs4 import BeautifulSoup
from django.db import models

HOST = 'www3.gobiernodecanarias.org'
URL_BASE = f'https://{HOST}/juriscan/ficha.jsp?id={{id_juriscan}}'


def obtener_titulo_desde_juriscan(id_juriscan: int) -> str|None:
    """A partir del número de ficha de Juriscan, devuelve el título.

    Si no se puede acceder a la página de Jurisca ya sea
    porque no exista la ficha, o porque Juriscán esté caido, o
    por cualquier otra razón, devolverá ``None``. Esto significa
    que una llamada posterior podría tener éxito, aun cuando
    la llamada actual falle.

    Ejemplo de uso:

        >>> txt = obtener_titulo_desde_juriscan(5559)
        >>> assert txt == 'Ley 2/1984, 11 abril, de Premios Canarias'
        >>>

    Parameters:

        id_juriscan (int): Número de la ficha de Juriscán

    Returns:

        (str) El título de la ficha, si se ha podido acceder a la
        página de Juriscán, o ``None`` si no se ha conseguido.

    """
    url = URL_BASE.format(id_juriscan=id_juriscan)
    with urlopen(url) as response:
        html = response.read().decode('iso-8859-1')
        soup = BeautifulSoup(html, features="html.parser")
        name = soup.find(id="titleFicha")
        if name:
            return name.text.strip()
    return None


class Juriscan(models.Model):

    class Meta:
        ordering = ['id_juriscan',]

    id_juriscan = models.BigIntegerField(primary_key=True)
    titulo = models.CharField(max_length=2280)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    checked = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

    @classmethod
    def load_juriscan(cls, pk:str):
        try:
            return cls.objects.get(id_juriscan=pk)
        except cls.DoesNotExist:
            return None

    def url(self):
        return URL_BASE.format(id_juriscan=self.id_juriscan)

    @classmethod
    def load_or_create(cls, id_juriscan):
        juriscan = cls.load_juriscan(id_juriscan)
        if not juriscan:
            titulo = obtener_titulo_desde_juriscan(id_juriscan)
            if titulo:
                juriscan = Juriscan(
                    id_juriscan=id_juriscan,
                    titulo=titulo,
                    )
                juriscan.save()
        return juriscan
    
    def necesita_actualizar(self):
        now = timezone.now()
        delta = now - self.checked
        return delta.days > 27


