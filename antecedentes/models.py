import uuid

from django.db import models

from sistemas.models import Usuario
from sistemas.models import Sistema


class TipoEvento(models.Model):

    class Meta:
        db_table = 'ant_tipo_evento'
        verbose_name = 'Tipo de evento'
        verbose_name_plural = 'Tipos de evento'

    id_tipo_evento = models.CharField(max_length=1, primary_key=True)
    nombre_tipo = models.CharField(max_length=28, unique=True)

    def __str__(self):
        return self.nombre_tipo


class Historico(models.Model):

    class Meta:
        abstract = True

    id_evento = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        )
    tipo_evento = models.ForeignKey(
        TipoEvento,
        on_delete=models.PROTECT,
        )
    descripcion = models.CharField(max_length=2048)
    f_evento = models.DateTimeField(auto_now_add=True, editable=False)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        editable=False,
        )

            
class HistoricoSistema(Historico):

    class Meta:
        db_table = 'ant_historico_sistema'
        verbose_name = 'Historico de sistema'
        verbose_name_plural = 'Historicos de sistemas'

    sujeto = models.ForeignKey(
        Sistema,
        related_name='historico',
        on_delete=models.CASCADE,
        )


class HistoricoUsuario(Historico):

    class Meta:
        db_table = 'ant_historico_usuario'
        verbose_name = 'Historico de usuario'
        verbose_name_plural = 'Historicos de usuarios'

    sujeto = models.ForeignKey(
        Usuario,
        related_name='historico',
        on_delete=models.CASCADE,
        )
