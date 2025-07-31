from django.db import models


class Tema(models.Model):

    class Meta:
        ordering = ['nombre_tema',]

    id_tema = models.CharField(max_length=3, primary_key=True)
    nombre_tema = models.CharField(max_length=32)
    transversal = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre_tema} ({self.id_tema})'


class Sistema(models.Model):

    class Meta:
        ordering = ['nombre',]

    id_sistema = models.BigAutoField(primary_key=True)
    dir3_id = models.CharField(max_length=9)
    codigo = models.CharField(max_length=32, unique=True)
    nombre = models.CharField(max_length=220)
    descripcion = models.CharField(max_length=512)
    explicacion = models.TextField(blank=True, default='')
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


    def __str__(self):
        return self.nombre
