#!/usr/bin/env python3

import uuid
from html import escape

from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce

from directorio.models import Organismo
from . import diagnosis
from . import links



class TemaManager(models.Manager):

    def with_counts(self):
        return self.annotate(num_sistemas=Coalesce(models.Count("sistemas"), 0))


class Tema(models.Model):

    class Meta:
        ordering = ['nombre_tema',]

    objects = TemaManager()

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

    def inicial(self):
        return self.nombre_tema[0].upper()


class Sistema(models.Model):

    class Meta:
        ordering = ['nombre',]

    id_sistema = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador público del sistema (UUID4)",
        )
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
        default='UNK',
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
    tiene_especial_importancia = models.BooleanField(
        default=False,
        help_text="Este S.I. contiene activos de datos de especial importancia",
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
    def alta_sistema(
            cls,
            nombre: str,
            codigo: str,
            proposito: str,
            organismo: Organismo,
            tema=None,
            ):
        """Dar de alta un nuevo sistema.

        Parameters:

            - nombre (str): Nombre del sistema
            - codigo (str): Código identificador del sistema
            - proposito (str): Propósito
            - organismo (Organismo): Instancia del organismo al que
                está asociado el sistema.
            - tema (Tema|None): Instacia del tema, o `None`

        Returns:

            La instancia de Sistema, ya alamacenada
            en la base de datos.
        """
        sistema = Sistema(
            nombre=nombre,
            codigo=codigo,
            proposito=proposito,
            organismo=organismo,
            tema=tema,
            )
        sistema.save()
        return sistema

    @classmethod
    def load_sistema(cls, pk:int):
        """Obtener un sistema a partir de su clave primaria.

        Parameters:

            pk (int): Clave primaria del sistema

        Returns:

            La instancia, si exciste el registro correspondiente
            en la base de datos, o `None` en caso contrario.

        """
        try:
            return cls.objects.get(id_sistema=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.nombre

    def url_detalle_sistema(self):
        """URL de detalle del sistema.
        """
        return links.a_detalle_sistema(self.pk)

    def get_estado(self) -> str:
        '''Calcula y devuelve el estado de madurez del sistema.

        Returns:

            str: Una cadena de texto con uno de los 
            siguiente posibles valores: `'green'`, `'yellow'` o
            `'red'`.
        '''
        flags = diagnosis.DiagnosticoSistema(self).flags()
        if all(flags):
            return 'green'
        if sum(flags) > 1:
            return 'yellow'
        return 'red'

    def asignar_tema(self, tema: Tema|str) -> Tema:
        '''Asignar un tema a un S.I. usando el código.

        El cambio se registra inmediatamente en la base de datos.

        Parameters:

            id_tema (str): Una instancioa de tema, o La clave 
                primaria del tema

        Returns:
            
            La instancia del tema.

        Exceptions:

            Eleva una excepción de tipo `ValueError` si el código
            de tema no existe en la base de datos.
        '''
        if not isinstance(tema, Tema):
            tema = Tema.load_tema(tema)
            if not tema:
                raise ValueError(
                    'El código de tema indicado:'
                    f' {escape(repr(tema))} no es válido'
                    )
        self.tema = tema
        self.save(update_fields=['tema'])
        return tema
        
    def asignar_organismo(self, organismo: Organismo|int) -> Organismo:
        '''Asignar un S.I. a un organismo.

        El cambio se registra inmediatamente en la base de datos.

        Parameters:

            organismo (Organismo|int): Una instancioa de tema, o La clave 
                primaria del tema

        Returns:
            
            La instancia del organismo.

        Exceptions:

            Eleva una excepción de tipo `ValueError` si el código
            del organismo no existe en la base de datos.
        '''
        if not isinstance(organismo, Organismo):
            organismo = Organismo.load_organismo(organismo)
        self.organismo = organismo
        self.save(update_fields=['organismo'])
        return organismo

    def asignar_responsable(self, cometido, usuario):
        '''Asigna a un sistema un responsable

        Un responsable es una persona con un cometido determinado.

        Es idempotente, si el resposable ya estaba
        creado, no hace nada.
        '''
        perfil, _created= Perfil.upsert(
            sistema=self,
            cometido=cometido,
            usuario=usuario,
            )
        return perfil


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

    class Meta:
        ordering = ['nombre', 'apellidos']

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

    def organismos_filtrados(self, query: str):
        return models.Organismo.search(query)

    def as_dict(self) -> dict:
        if self.is_valid():
            return {
                name: self.cleaned_data[name]
                for name in self.Meta.fields
                }
        return {}

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

    @classmethod
    def search_usuarios(cls, query):
        return (
            cls.objects.filter(
                Q(login__icontains=query) |
                Q(email__icontains=query) |
                Q(nombre__icontains=query) |
                Q(apellidos__icontains=query)
                )
            )

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

    @classmethod
    def load_perfil(cls, pk:int):
        '''Devuelve la instancia del perfil por clave primaria.

        O `None` si no existe perfil con esa clave.
        '''
        try:
            return cls.objects.get(id_perfil=pk)
        except cls.DoesNotExist:
            return None

    @classmethod
    def upsert(cls, sistema, usuario, cometido):
         perfil, created = cls.objects.update_or_create(
            sistema=sistema,
            usuario=usuario,
            cometido=cometido,
            )
         return perfil, created

    def __str__(self):
        return f"{self.get_cometido_display()} de {self.sistema.codigo}"

