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

    @classmethod
    def load_tema(cls, pk:str):
        try:
            return cls.objects.get(id_tema=pk)
        except cls.DoesNotExist:
            return None


class Sistema(models.Model):

    class Meta:
        ordering = ['nombre',]

    id_sistema = models.BigAutoField(primary_key=True)
    nombre = models.CharField(
        max_length=220,
        unique=True,
        help_text="Nombre del sistema",
        )
    organismo = models.ForeignKey(
        Organismo,
        related_name='sistemas',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        )
    codigo = models.SlugField(
        max_length=32,
        help_text="Código identificador del sistema (una sola palabra)",
        unique=True,
        )
    url = models.URLField(
        max_length=720,
        default=None,
        blank=True,
        null=True,
        )
    descripcion = models.TextField(
        max_length=512,
        blank=True,
        default='',
        verbose_name="Descripción del sistema",
        )
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


class Usuario(models.Model):
    login = models.CharField(max_length=32, primary_key=True)
    email = models.CharField(max_length=384, unique=True)
    nombre = models.CharField(
        max_length=96,
        blank=True,
        null=True,
        default=None,
        )
    apellidos = models.CharField(
        max_length=192,
        blank=True,
        null=True,
        default=None,
        )
    organismo = models.ForeignKey(
        Organismo,
        related_name='usurios',
        on_delete=models.PROTECT,
        )
    f_alta = models.DateTimeField(auto_now_add=True)
    f_cambio = models.DateTimeField(auto_now=True)
    f_baja = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        )

    @classmethod
    def load_usuario(cls, pk:str):
        try:
            return cls.objects.get(login=pk)
        except cls.DoesNotExist:
            return None

    def nombre_completo(self):
        if self.nombre:
            if self.apellidos:
                return f'{self.nombre} {self.apellidos}'
            return self.nombre
        return self.login

    def __str__(self):
        return self.nombre_completo()


class Interlocutor(models.Model):

    class Meta:
        verbose_name = 'Interlocutor'
        verbose_name_plural = 'Interlocutores'

    id_interlocutor = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        related_name='interlocutor_de',
        on_delete=models.CASCADE,
        )
    organismo = models.ForeignKey(
        Organismo,
        related_name='interlocutores',
        on_delete=models.PROTECT,
        )
    f_alta = models.DateTimeField(auto_now_add=True)
    f_cambio = models.DateTimeField(auto_now=True)
    f_baja = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        )

    @classmethod
    def upsert(cls, usuario, organismo):
         interlocutor, created = cls.objects.update_or_create(
            usuario=usuario,
            organismo=organismo,
            )
         return interlocutor, created


class Perfil(models.Model):

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    COMETIDOS = [
        ('FUN', 'Responsable funcional'),
        ('TEC', 'Responsable técnico'),
        ('PDD', 'Protección de datos'),
        ('INT', 'Interlocutor'),
        ]
    id_perfil = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        related_name='perfiles',
        on_delete=models.CASCADE,
        )
    cometido = models.CharField(max_length=3, choices=COMETIDOS)
    sistema = models.ForeignKey(
        Sistema,
        related_name='perfiles',
        on_delete=models.CASCADE,
        )
    f_alta = models.DateTimeField(auto_now_add=True)
    f_cambio = models.DateTimeField(auto_now=True)
    f_baja = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        )

    def __str__(self):
        return f"{self.get_cometido_display()} de {self.sistema.codigo}"

    @classmethod
    def upsert(cls, usuario, organismo, cometido):
         perfil, created = cls.objects.update_or_create(
            usuario=usuario,
            organismo=organismo,
            cometido=cometido,
            )
         return perfil, created
