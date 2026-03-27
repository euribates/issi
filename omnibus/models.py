#!/usr/bin/env python3

import uuid
import json

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder



MAX_LENGTH_FOR_PRIMARY_KEY = 32
MAX_LENGTH_FOR_CLASS_NAME = 48
MAX_LENGTH_FOR_DESCRIPTION = 2048
MAX_LENGTH_FOR_USERNAME = 62


class NivelEvento(models.Model):
    """Nivel del evento

    Estos son los niveles predefinidos:

    | nivel   | descripción                      |
    |:-------:|:---------------------------------|
    | debug   | Mensajes de depuración           |
    | info    | Mensajes informativos            |
    | insert  | Alta de nuevos datos             |
    | update  | Modificación de datos existentes |
    | delete  | Borrado de datos existentes      |
    | archive | Borrado lógico o archivado       |
    | warning | Mensajes de aviso                |
    | error   | Mensajes de error                |
    | panic   | Mensaje de error crítico         |

    Los niveles ``insert``, ``update``, ``archive`` y ``delete`` se
    consideran subtipos concretos del tipo ``info``.
    """

    class Meta:
        """Metadatos de la clase NivelEvento.
        """
        db_table = 'obus_nivel_evento'
        verbose_name = 'Nivel del evento'
        verbose_name_plural = 'Niveles de los eventos'

    id_nivel_evento = models.CharField(max_length=8, primary_key=True)
    nombre_nivel = models.CharField(max_length=28, unique=True)

    def __str__(self) -> str:
        return self.nombre_nivel

    def to_json(self) -> str:
        """Devuelve una representación textual en formato json.
        """
        return json.dumps({
            'id_nivel_evento': self.id_nivel_evento,
            'nombre_nivel': self.nombre_nivel,
            }, indent=4)


class Evento(models.Model):
    """Un evento (cambio de estado) de un objeto.

    Campos:

    - id_evento (``UUID``): Clave primaria del evento. Por defecto usa
      ``uuid.uuid1``.

    - nivel_evento (``str``): Nivel del evento. Es una clave foránea a
      ``NivelEvento``, donde se registran los diferentes tipos de
      niveles de evento disponibles.

    - sujeto (``str``): La clave primaria, en JSON, del objeto cuyo
      estado ha sido modificado. El valor pasado se pasa por
      ``json.dumps``.

      Es una clave foránea, pero no se implementa como tal para
      simplificar el sistema y que se pueda adaptar a cualquier modelo.

      Esto complica el acceso a los eventos desde el punto de vista del
      objeto, pero simplifica por otro lado al no tener que mantener una
      clave foránea y se puede adaptar por tanto a casi cualquier
      sistema (siempre que la representación de la clave foránea quepa
      en 32 caracteres).

    - nombre_clase (``str``): El nombre de la clase del sujeto. En
      principio con esta información y la representación de la clave
      primaria debería bastar para poder identificar al sujeto en la
      base de datos.

    - descripcion (``str``): Descripción textual del cambio sufrido por
      el modelo.

    - momento (datetime.datetime): Fecha y hora del momento del cambio.
      Si no se especifica --que es lo normal--, se usará la fecha y hora
      en que se almace en la base de datos.

    - usuario (usr): Identificación del usuario que ha provocado el
      cambio. Idealmente, el ``login`` o ``username`` del usuario. Al
      igual que con el campo ``sujeto``, debería ser un ``ForeignKey`̀a
      la clase ``User`` o similar, pero se deja abierto para hacer el
      sistema más flexible y capaz de funcionar con otros sistemas de
      autenticación, aparte del de Django.

    - payload (str): Una representación en JSON de la instancia en
      el momento del cambio.
    """

    class Meta:
        """Metadatos de la case Evento.

        """
        db_table = 'obus_evento'
        verbose_name = 'evento'
        verbose_name_plural = 'eventos'
        ordering = ['momento']

    id_evento = models.UUIDField(
        primary_key=True,
        default=uuid.uuid1,
        editable=False,
        )
    nivel_evento = models.ForeignKey(
        NivelEvento,
        on_delete=models.PROTECT,
        )
    sujeto = models.CharField(max_length=MAX_LENGTH_FOR_PRIMARY_KEY)
    nombre_clase = models.CharField(max_length=MAX_LENGTH_FOR_CLASS_NAME)
    descripcion = models.CharField(max_length=MAX_LENGTH_FOR_DESCRIPTION)
    momento = models.DateTimeField(auto_now_add=True, editable=False)
    usuario = models.CharField(max_length=MAX_LENGTH_FOR_USERNAME)
    payload = models.JSONField(
        encoder=DjangoJSONEncoder,
        blank=True,
        default=None,
        null=True,
        )

    def __str__(self):
        return f'{self.nombre_clase}/{self.sujeto}:{self.nivel_evento}'

    @classmethod
    def new(cls, item, msg, level, username):
        _primary_key = json.dumps(item.pk)[:MAX_LENGTH_FOR_PRIMARY_KEY]
        _class_name = item.__class__.__name__[:MAX_LENGTH_FOR_CLASS_NAME]
        _descripcion = msg[:MAX_LENGTH_FOR_DESCRIPTION]
        _username = str(username)[:MAX_LENGTH_FOR_USERNAME]
        if hasattr(item, 'as_dict') and callable(item.as_dict):
            payload = item.as_dict()
        else:
            payload = None
        event = cls(
            nivel_evento_id=level,
            sujeto=_primary_key,
            nombre_clase=_class_name,
            descripcion=_descripcion,
            usuario=_username,
            payload=payload,
            )
        event.save()
        return event
