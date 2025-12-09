#!/usr/bin/env python3

from datetime import datetime as DateTime
from html import escape
from pathlib import Path
from urllib.request import urlretrieve
from uuid import uuid4, UUID

from bs4 import BeautifulSoup
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.utils.timezone import localtime

from directorio.models import Organismo
from . import diagnosis
from . import links


#~ Dominio para correo electrónico
EMAIL_DOMAIN = 'gobiernodecanarias.org'

#~ Directorio temporal
TEMP_DIR = settings.BASE_DIR / Path('temp')
if not TEMP_DIR.is_dir():
    TEMP_DIR.mkdir()


class FamiliaManager(models.Manager):

    def with_counts(self):
        return self.annotate(num_sistemas=Coalesce(models.Count("sistemas"), 0))


class Familia(models.Model):

    class Meta:
        ordering = ['id_familia',]

    id_familia = models.CharField(max_length=3, primary_key=True)
    nombre_familia = models.CharField(max_length=128)

    objects = FamiliaManager()

    @classmethod
    def load_familia(cls, pk:str):
        try:
            return cls.objects.get(id_familia=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self) -> str:
        return self.nombre_familia

    def no_definida(self) -> bool:
        return self.pk == 'UNK'


class TemaManager(models.Manager):


    def with_counts(self):
        return self.annotate(num_sistemas=Coalesce(models.Count("sistemas"), 0))


class Tema(models.Model):

    class Meta:
        ordering = ['nombre_tema',]

    objects = TemaManager()

    id_tema = models.CharField(max_length=3, primary_key=True)
    nombre_tema = models.CharField(max_length=96)
    transversal = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_tema

    @classmethod
    def load_tema(cls, pk:str):
        try:
            return cls.objects.get(id_tema=pk)
        except cls.DoesNotExist:
            return None

    @classmethod
    def load_tema_por_nombre(cls, nombre:str):
        try:
            return cls.objects.get(nombre_tema=nombre)
        except cls.DoesNotExist:
            return None

    def inicial(self) -> str:
        return self.nombre_tema[0].upper()

    def no_definido(self) -> bool:
        return self.pk == 'UNK'


class Sistema(models.Model):
    """Modelo Sistemas de Información.
    """

    class Meta:
        """Opciones para modelo Sistema.
        """
        ordering = ['nombre_sistema',]

    id_sistema = models.BigAutoField(primary_key=True)
    uuid_sistema = models.UUIDField(
        default=uuid4,
        editable=False,
        help_text="Identificador público del sistema (UUID)",
        unique=True,
        )
    nombre_sistema = models.CharField(
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
        blank=True,
        default='',
        verbose_name="Descripción del sistema",
        )
    proposito = models.TextField(
        blank=True,
        default='',
        verbose_name="Propósito",
        )
    observaciones = models.TextField(
        blank=True,
        default='',
        verbose_name="Observaciones",
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
    familia = models.ForeignKey(
        Familia,
        default='UNK',
        help_text="Indica la familia, si procede",
        related_name='sistemas',
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
    f_alta = models.DateTimeField(auto_now_add=True)
    f_cambio = models.DateTimeField(auto_now=True)
    f_baja = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        )

    @classmethod
    def alta_sistema(
            cls,
            nombre_sistema: str,
            codigo: str,
            proposito: str,
            organismo: Organismo,
            tema=None,
            ):
        """Dar de alta un nuevo sistema.

        Parameters:

            - nombre_sistema (str): Nombre del sistema
            - codigo (str): Código identificador del sistema
            - proposito (str): Propósito
            - organismo (Organismo): Instancia del organismo al que
                está asociado el sistema.
            - tema (Tema|None): Instacia del tema, o `None`

        Returns:

            La instancia de Sistema, ya almacenada
            en la base de datos.
        """
        sistema = Sistema(
            nombre_sistema=nombre_sistema,
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

            La instancia, si existe el registro correspondiente
            en la base de datos, o `None` en caso contrario.

        """
        try:
            return cls.objects.get(id_sistema=pk)
        except cls.DoesNotExist:
            return None

    @classmethod
    def load_sistema_por_uuid(cls, uuid:str|UUID):
        """Obtener un sistema a partir de su clave secundaria UUID

        Parameters:

            uuid (str|UUID): Clave secundaria del sistema

        Returns:

            La instancia, si existe el registro correspondiente
            en la base de datos, o `None` en caso contrario.

        """
        try:
            return cls.objects.get(uuid_sistema=uuid)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.nombre_sistema

    def touch(self):
        self.f_cambio = localtime()
        self.save(update_fields=['f_cambio'])
        self.organismo.touch()

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

            tema (Tema|str): Una instancia de tema, o la clave 
                primaria del tema.

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

    def asignar_familia(self, familia: Familia|str) -> Familia:
        '''Asignar una familia a un S.I. usando el código o la familia.

        El cambio se registra inmediatamente en la base de datos.

        Parameters:

            `familia` (str|Familia): Una instancia de la familia, o la
            clave primaria de la familia.

        Returns:
            
            La instancia de la familia.

        Exceptions:

            Eleva una excepción de tipo `ValueError` si el código
            de familia no existe en la base de datos.
        '''
        if not isinstance(familia, Familia):
            familia = Familia.load_familia(familia)
            if not familia:
                raise ValueError(
                    'El código de familia indicado:'
                    f' {escape(repr(familia))} no es válido'
                    )
        self.familia = familia
        self.save(update_fields=['familia'])
        return familia

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


def importar_sistemas_desde_fichero(stream):
    import csv
    from . import parsers
    reader = csv.reader(stream, delimiter=',', quotechar='"')
    _first_line = next(reader)      # Ignoramos la primera fila
    for n_linea, tupla in enumerate(reader, start=1):
        errors, payload = parsers.parse_row(tupla, n_linea=n_linea)
        yield errors, payload


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
    f_alta = models.DateTimeField(auto_now_add=True)
    f_cambio = models.DateTimeField(auto_now=True)
    f_baja = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        )


    def __str__(self):
        return self.nombre_activo

    def touch(self):
        self.f_cambio = localtime()
        self.save()
        self.sistema.touch()



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
        related_name='usuarios',
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

    @classmethod
    def search_usuarios(cls, query):
        return (
            cls.objects.filter(
                Q(login__icontains=query) |
                Q(email__icontains=query) |
                Q(nombre_sistema__icontains=query) |
                Q(apellidos__icontains=query)
                )
            )

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = f'{self.login}@{EMAIL_DOMAIN}'
        super().save(*args, **kwargs)

    def nombre_completo(self):
        if self.nombre:
            if self.apellidos:
                return f'{self.nombre} {self.apellidos}'
            return self.nombre
        return self.login

    def abreviado(self):
        if self.email.lower().endswith('gobiernodecanarias.org'):
            return self.login
        return self.email

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


class NormativaSistemaManager(models.Manager):

    def get_by_natural_key(self, id_sistema, num_juriscan):
        return self.get(id_sistema, num_juriscan)


class NormaSistema(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sistema", "num_juriscan"],
                name="unique_sistema_juriscan",
                ),
            ]

    id_normativa = models.BigAutoField(primary_key=True)
    sistema = models.ForeignKey(
        Sistema,
        related_name='normativa',
        on_delete=models.CASCADE,
        )
    num_juriscan = models.PositiveIntegerField()
    resumen = models.CharField(
        max_length=2048,
        null=True,
        default=None,
        blank=True,
        )
    f_alta = models.DateTimeField(auto_now_add=True)
    f_cambio = models.DateTimeField(auto_now=True)
    f_baja = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        )

    def natural_key(self) -> tuple[int, int]:
        '''Devuelve una tupla con los valores de la clave natural.
        '''
        return (self.sistema.pk, self.num_juriscan)

    def __str__(self):
        return 'Juriscan/{self.num_juriscan}'

    @classmethod
    def upsert(cls, sistema, num_juriscan: int) -> tuple:
        """Actualiza o inserta la norma del sistema, según proceda.

        Es idempotente; si el sistema ya está vinculado a ese
        código de Juriscán, no hace nada.

        Patrameters:

            sistema: Sistema - El sistema al que se le va a asignar la norma.

            num_juriscan: int - El código o número Juriscan de la norma.

        Returns:
            
            Una dupla, en la que el primer elemento
            es la instancia recién creada o actualizada
            y el segundo un booleano indicando si ha
            sido creado (`True`) o modificado (`False`).
        """
        norma_sistema, created = cls.objects.update_or_create(
            sistema=sistema,
            num_juriscan=num_juriscan,
            )
        return norma_sistema, created


class Ente(models.Model):

    DATOS = 'datos.canarias.es'
    VALID_DAYS = 14

    class Meta:
        ordering = [
            'peso',
            'organismo__nombre_organismo',
            ]

    id_ente = models.SlugField(
        max_length=12,
        primary_key=True,
        )
    organismo = models.OneToOneField(
        Organismo,
        related_name='ente',
        on_delete=models.PROTECT,
        )
    peso = models.IntegerField(default=100)
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

    def __str__(self) -> str:
        return f'{self.organismo.nombre_organismo} ({self.pk})'

    def es_de_primer_nivel(self) -> bool:
        result = self.organismo.categoria in {
            'Presidencia',
            'Consejería',
            'Viceconsejería',
            }
        return result

    def sistemas_del_ente(self):
        from sistemas.models import Sistema
        return (
            Sistema.objects
            .select_related('organismo')
            .filter(organismo__ruta__startswith=self.organismo.ruta)
            )

    def descargar_datos(self, url, force=False):
        slug = url.rsplit('/', 1)[1]
        filename = Path(f'{slug}.html')
        target_file = TEMP_DIR / Path(filename)
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
        if not url:
            return
        with open(self.descargar_datos(url), 'r', encoding='utf-8') as source:
            soup = BeautifulSoup(source, 'html.parser')
            for item in soup.find_all('li', 'dataset-item'):
                href = item.a.attrs['href']
                url = f'https://{self.DATOS}/{href}'
                desc = ''.join(item.a.contents)
                yield(url, desc)


    def asignar_interlocutor(self, usuario):
        '''Asigna un interlocutor al ente

        Es idempotente, si el interlocutor ya estaba
        asignado, no hace nada.
        '''
        from sistemas.models import Interlocutor
        interlocutor, _created = Interlocutor.upsert(
            organismo=self.organismo,
            usuario=usuario,
            )
        return interlocutor

