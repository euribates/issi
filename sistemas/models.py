from django.db import models

from directorio.models import Organismo
from . import links


class Tema(models.Model):

    class Meta:
        ordering = ['nombre_tema',]

    id_tema = models.CharField(max_length=3, primary_key=True)
    nombre_tema = models.CharField(max_length=32)
    transversal = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_tema


class Sistema(models.Model):

    class Meta:
        ordering = ['nombre',]

    id_sistema = models.BigAutoField(primary_key=True)
    organismo = models.ForeignKey(
        Organismo,
        related_name='sistemas',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        )

    dir3_id = models.CharField(max_length=9)
    codigo = models.CharField(max_length=32, unique=True)
    nombre = models.CharField(max_length=220)
    url = models.URLField(
        max_length=720,
        default=None,
        blank=True,
        null=True,
        )
    descripcion = models.TextField(max_length=512)
    proposito = models.TextField(
        blank=True,
        default='',
        verbose_name="Propósito",
        )
    tema = models.ForeignKey(
        Tema,
        related_name='sistemas',
        on_delete=models.PROTECT,
        )
    es_transversal = models.BooleanField(
        default=False,
        help_text=(
            "Este S.I. es horizontal a todos"
            " los departamentos."
            )
        )
    es_subsistema_de = models.ForeignKey(
        "Sistema",
        null=True,
        blank=True,
        default=None,
        help_text="Es un subsistema de otro S.I.",
        related_name='subsistemas',
        on_delete=models.PROTECT,
        )
    icono_height = models.PositiveIntegerField(default=0)
    icono_width = models.PositiveIntegerField(default=0)
    icono = models.ImageField(
        upload_to="sistemas/iconos/%Y/",
        blank=True,
        null=True,
        default=None,
        height_field='icono_height',
        width_field='icono_width',
        max_length=512,
        )
    responsable_funcional = models.CharField(
        max_length=32,
        default=None,
        blank=True,
        null=True,
        )
    responsable_tecnico = models.CharField(
        max_length=32,
        default=None,
        blank=True,
        null=True,
        )

    @classmethod
    def load_sistema(cls, pk:int):
        try:
            return cls.objects.get(id_sistema=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.nombre

    def url_detalle_sistema(self):
        return links.a_detalle_sistema(self.pk)


class Activo(models.Model):

    NIVELES_DATOS_PERSONALES = [
        ('NO', 'No contiene datos personales'),
        ('DP', 'Contiene datos personales'),
        ('XS', 'Contiene datos personales especialmente sensibles'),
        ]

    id_activo = models.BigAutoField(primary_key=True)
    sistema = models.ForeignKey(
        Sistema,
        related_name='activos',
        on_delete=models.PROTECT,
        )
    nombre_activo = models.CharField(max_length=288)
    descripcion = models.TextField()
    es_prioritario = models.BooleanField(default=False)
    esta_georeferenciado = models.BooleanField(default=False)
    datos_personales = models.CharField(
        max_length=2,
        choices=NIVELES_DATOS_PERSONALES,
        default='NO',
        )

    def __str__(self):
        return self.nombre_activo
