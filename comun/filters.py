#!/usr/bin/env python

import re
from urllib.parse import urlparse
from html import escape

"""
Estos filtros son funciones que esperan un único parámetro y devuelven
un único resultado. Están pensados sobre todo para limpiar o representar
datos en distintos formatos.

"""


def clean_text(text: str) -> str|None:
    """Limpia el formato de texto.

    - Si hay espacios al principio o al final se eliminan
    - Si tiene comillas dobles al principio y al final las elimina.
    - Si tiene comillas simples al principio y al final las elimina.
    - Si tiene triples comillas dobles al principio y al final las elimina.
    - Si tiene triples comillas simples al principio y al final las elimina.
    - Si no hay texto, se devuelve ``None``.

    >>> assert clean_text('"hola"') == 'hola'
    >>> assert clean_text('') is None

    Parameters:
        
        text (str): La cadena de texto a limpiar.

    Returns:

        Una cadena de texto limpia.
    """
    if text is None:
        return None
    text = text.strip()
    if text in {'', '_U'}:
        return None
        text = str(text)
    if len(text) > 5:
        if text[:3] == text[-3:] == '"""':
            return text[3:-3]
        if text[:3] == text[-3:] == "'''":
            return text[3:-3]
    if text[0] == text[-1] == '"':
        return text[1:-1]
    if text[0] == text[-1] == "'":
        return text[1:-1]
    return text


def clean_integer(text: str) -> int|None:
    """Interpreta una cadena de texto como un número entero.

    Los valores especiales ``''`` (cadena vacia) o ``'_U'`` se 
    interpretan como ``None``.

    >>> assert clean_integer('123') == 123
    >>> assert clean_integer('_U') is None

    Parameters:

        text (str): Una cadena de texto que contiene un número
                    entero, como ``'123'``.

    Returns:

        Un entero, o ``None``.
    """
    text = clean_text(text)
    if text is None:
        return text
    if not text.isdigit():
        raise ValueError(
            f"El valor indicado: {escape(text)}"
            " no parece un número entero."
            )
    return int(text) if text else None


def clean_url(url: str) -> str:
    """Limpia el formato de texto de una url.

    - Si ``url`` es nulo, vacio o el valor ``_U`` se devuelve ``None``
    - Verifica que empieza por ``http``
    - Realiza las mismas operaciones de limpieza que 
      :py:func:`clean_text`:

    >>> assert clean_url('http://www.python.org/') == 'http://www.python.org/'
    >>> assert clean_url(None) == None
    >>> assert clean_url('') == None
    >>> assert clean_url('_U') == None

    Params:
        
        - url (str): La cadena de texto con la URL a limpiar.

    Returns:

        Una cadena de texto con la URL limpia, o ``None``. Si la entrada
        no es vacia paro no tiene el formato de una URL se eleva la
        excepcion :py:exc:`ValueError`.
    """

    if url in {'_U', '', None}:
        return None
    url = clean_text(url)
    parts = urlparse(url)
    if parts.scheme not in {'http', 'https'}:
        raise ValueError(
            f"El valor indicado: {escape(url)}"
            " no parece tener el formato correcto."
            )
    return url


_SLUGIFY_MAP = {
    32: 95,  # space -> hyphen
    33: None,  # exclamation mark
    34: None,  # double quotes
    35: None,  # hash
    36: None,  # dollar
    37: None,  # percent
    38: None,  # ampersand
    39: None,  # simple quote
    40: None,  # open par
    41: None,  # close par
    42: None,  # asterisk
    43: 95,  # plus -> hyphen
    44: None,  # comma
    46: None,  # dot or full stop
    47: 95,  # slash -> hyphen
    58: 95,  # colon -> hyphen
    59: 95,  # semicolon -> hyphen
    60: None,  # open angled bracket
    61: 95,  # equals -> hyphen
    62: None,  # close angled bracket
    63: None,  # question mark
    64: 95,  # @ -> hyphen
    91: None,  # open bracket
    92: 95,  # backslash -> hyphen
    93: None,  # close bracket
    94: 95,  # caret -> hyphen
    96: None,  # grave accent
    123: None,  # open brace
    124: 95,  # pipe -> hyphen
    125: None,  # close brace
    126: 95,  # equivalency sign (~) -> hyphen
    133: 95,  # ellipsis
    191: None,  # open question mark
    193: 65,
    201: 69,
    205: 73,
    209: 78,
    211: 79,
    218: 85,
    220: 85,
    225: 97,  # a
    233: 101,
    237: 105,
    241: 110,
    243: 111,
    250: 117,
    252: 117,
    8230: 95,  # ellipsis
}

_SLUGIFY_PAT_MULTIPLE_HYPHENS = re.compile(r'--+')


def slugify(texto: str) -> str:
    """Transforma texto a un valor válido para usarse como *slug*.

    Sustituye espacios por el caracter ``'_'``, elimina caracteres
    especiales, convierte vocales acentuadas, reduce repeticiones,
    convierte mayúsculas a minúsculas y otras modificaciones que
    permiten usar el resultado como un valor seguro para ser usado como
    nombre de fichero, parte de la URL, etc.

    >>> slugify('Hola, mundo') == 'hola_mundo'

    Parameters:

        text (str): El texto a transformar

    Returns:

        Una cadena de texto apta para ser usada como nombre de un fichero,
        parte de una URL, etc. 
    """
    result = texto.lower()
    result = result.replace('ñ', 'nn')
    result = result.replace('€', '-euros')
    result = result.translate(_SLUGIFY_MAP)
    result = ''.join([_ for _ in result if ord(_) < 129])
    result = _SLUGIFY_PAT_MULTIPLE_HYPHENS.sub('_', result)
    return result


def codigos_renombrados(codigo):
    tabla = {
        'Registro de Plantaciones de Viñedo': 'REGPLANVID',
        'Registro de Sociedades Agrarias de Transformación de Canarias': 'REGSOCAGR',
        'APP Móvil': 'APP_MOVIL_CAPGA',
        'LicenciasPesca': 'LICENCIAS_PESCA',
        'Plataforma de Interoperabildad CAGPA': 'INTEROP_CAGPA',
        'RegistroProductores': 'REG_PRODUCTORES',
        'TrabajoPalmeras': 'TRABAJO_PALMERAS',
        'Centros de Día': 'CENTROS_DIA',
        'Centros de menores': 'CENTROS_MENORES',
        'EntidadesBS': 'REG_ENTIDADES',
        'Expedientes de Asesoría Jurídica': 'EXP_ASESORIA_JURIDICA',
        'Expedientes Régimen Júridico': 'EXP_REGIMEN_JURIDICO',
        'Familias Numerosas': 'EXP_FAMILIAS_NUMEROSAS',
        'Fondos Europeos': 'FONDOS_EUROPEOS',
        'Gestor de incidencias BS': 'GESTOR_INCIDENCIAS_BS',
        'Inspección de Centros': 'INSPECCION_CENTROS',
        'Intercambio de Ficheros Ministerios': 'INTEROP_MINISTERIO',
        'Justicia Juvenil': 'JUSTICIA_JUVENIL',
        'Pensiones': 'EXP_PENSIONES',
        'PersonalBS': 'PERSONAL_BS',
        'SITA-RCC': 'SITA_RCC',
        'Registro SIBS': 'REG_SIBS',
        'Registro del Menor': 'REG_MENORES',
        'Registro perros de asistencia': 'REG_PERROS_ASISTENCIA',
        'Subvención ITC': 'SUBVENCIONES_ITC',
        'SubvencionesBS': 'SUBVENCIONES_BS',
        'E-SEMANTICA': 'E_SEMANTICA',
        'E-OPERACIONES': 'E_OPERACIONES',
        'M4 PNet – NOMINA': 'M4_PNET_NOMINA',
        'SIRHUS Personal': 'SIRHUS',
        'ENTORNO DE TRABAJO COLABORATIVO Y MOODLE GESTION CONOCIMIENTO': 'ENTORNO_COLABORATIVO',
        'PUNTOS DE INFORMACION': 'PUNTOS_INFORMACION',
        'AGENDA DE JUICIOS RAPIDOS': 'AGENDA_JUICIOS_RAPIDOS',
        'AINOA (Cliente SAP)': 'AINOA',
        'OFICINA DE ASISTENCIA A LAS VÍCTIMAS DEL DELITO': 'OFICINA_ASISTENCIA_VICTIMAS_DELITO',
        'WEB INTERINOS DGRAJ': 'WEB_INTERINOS_JUSTICIA',
        'SIGAP-PAC': 'SIGAP_PAC',
        'PLANIFICACION SIGAP-PAC': ' PLANIFICACION_SIGAP-PAC',
        'SIGESCA 2.0': 'SIGESCA_2',
        'PAREJAS DE HECHO': 'REG_PAREJAS_HECHO',
        'REGISTRO DE COLEGIOS PROFESIONALES': 'REG_COLEGIOS_PROFESIONALES',
        'REGISTRO DE FUNDACIONES': 'REG_FUNDACIONES',
        'SOLICITUDES DE ACCESO A LA INFORMACIÓN PÚBLICA (RSAIP)': 'RSAIP',
        'ELECCIONES 2019': 'ELECCIONES_2019',
        'SITA-GOBABIERTO': 'SITA_GOBABIERTO',
        'GEBOC USAD': 'GEBOC_USAD',
        'LIBRO AZUL GESTION': 'LIBRO_AZUL',
        'PROHIBIDOS DEL JUEGO': 'PROHIBIDOS_JUEGO',
        'REGISTRO DEL JUEGO': 'REG_JUEGO',
        'SERVICIOS ELECTRONICOS PARA LA GESTION DEL JUEGO': ' REG_JUEGO_PLATEA',
        'ANIMALES DE COMPAÑÍA': 'REG_ANIMALES_DOM',
        'SITA-RAV': 'SITA_RAV',
        'SEDEe': 'SEDE_ELECTRONICA',
        'SEDEp': 'SEDE_PRESENCIAL',
        'SEDEep': 'SEDE_EMPLEADO_PUBLICO',
        'Sita-secura': 'SITA_SECURA',
        'infoplayas': 'INFOPLAYAS',
        'RETAMA-IP': 'RETAMA_IP',
        'EST-RECU': 'EST_RECU',
        'RedEXOS': 'RED_EXOS',
        'RedPromar': 'RED_PROMAR',
        'Red Vigía Canarias': 'RED_VIGIA',
        'Banco de imágenes P.N. Timanfaya': 'BANCO_IMAGENES_TIMANFAYA',
        'Herramienta de anonimización': 'ANONIMIZADOR',
        'Gestión de Comisiones de Servicios': 'GEST_COMISIONES_SERVICIOS',
        'Alta de Usuarios Comisiones de Servicios': 'ALTA_USUARIOS_COMISIONES_SERVICIOS',
        'Escuela de Pacientes': 'ESCUELA_PACIENTES',
        'Drago AE - Selene': 'DRAGO_SELENE',
        'ECG - Sistema de gestión de Electros': 'ECG',
        'miSCS': 'MISCS',
        'DragoFARMA': 'DRAGO_FARMA',
        'REC-SCS': 'RECETA_ELECTRONICA_SCS',
        'RESNS': 'RECETA_ELECTRONICA_SNS',
        'Sistemas Dinámicos de Adquisición': 'SISTEMAS_DINAMICOS_ADQUISICION',
        'AccesoUnico': 'ACCESO_UNICO',
        'PPCM-PACS': 'PPCM_PACS',
        'PPCM-RIS': 'PPCM_RIS',
        'REGOB / REOBEU': ' REGOB_REOBEU',
        'Registro de Farmacias': 'REG_FARMACIAS',
        '3M-Ayuda a la codificación': '3M_AYUDA_CODIFICACION',
        'Lista de Espera': 'LISTA_ESPERA',
        'Matadero': 'MATADERO_GC',
        'Actas de Inspección': 'ACTAS_INSPECCION',
        'Cartera de Servicios': 'CARTERA_SERVICIOS',
        'Hipoacusia': 'HIPOACUSIA',
        'M@GIN': 'MAGIN',
        'Cuadro de Mando Integrado de Turismo': 'CMI_Turismo',
        }
    return tabla.get(codigo, codigo)
