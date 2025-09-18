## ISSI - Inventario de sistemas de información

Este software es un prototipo para la implementación de un sistema de
inventario de sistemas de información.

### Qué es un sistema de información

En el contexto del presente proyecto, usaremos la siguiente definición
de un sistema de información:


> Conjunto de elementos (personas, procesos, datos, tecnología
> y recursos) que trabajan juntos para recopilar, procesar, almacenar,
> distribuir y gestionar información con el fin de apoyar la toma de
> decisiones, la coordinación operativa y el control dentro de una
> organización. 

Pero, qué **no** es un sistema de información:

- No es (necesariamente) una aplicación informática (aunque a menudo lo
  sea)

- Puede incluir **más de una** aplicación informática

- Puede **no tener ninguna** aplicación informática


En el sistema de inventario se propone solo **inventariar** cada
sistema, junto con los **activos de datos** que gestiona. Si se quiere
incluir un mayor detalle que incluya las personas, procesos, datos y
recursos asociados, estos se gestionan en un nivel superior.

## Algunos aspectos claves

- El acceso a la consulta del inventario es completa para cualquier
  persona perteneciente a las administraciones públicas de la Comunidad
  Autónoma de Canarias.

- También sera completa el acceso a la consulta por parte de cualquier
  persona previamente autorizada por una persona perteneciente al
  Gobierno de Canarias.

- Algunos datos del inventario podrán ser publicados como datos
  abiertos.


## Pistas de información para descubrir sistemas de información

## Algunos ejemplos de sistemas de información

- **AGENDA DE CARGOS PÚBLICOS**

    Proposito: Dar publicidad a las agendas de los cargos públicos en un
    ejercicio de transparencia del Gobierno de Canarias.

- **GEBOC** y **GEBOC USAD**

    Propósito: Gestión interna del BOC (Boletín Oficial de Canarias).


- **COETL**

    Propósito: Sistema de Gestión de las ETL, es decir, operaciones de
    extracción, transformación y carga (_[Extract, load and
    transform](https://es.wikipedia.org/wiki/Extract,_transform_and_load))
    de datos.

- **DIRCAC**

    Propósito: Directorio de Unidades Administrativas y Oficinas de
    Registro de las APCAC


- **ESB**

    Propósito: Plataforma de interoperabilidad de RRHH Plataforma de
    Interoperabilidad de RRHH

- **GDI**

    Propósito: Gestión de Identidades. Incluye plataforma MiClave

- **HIPERREG**

    Propósito: Sistema de Gestión Registral

- **JUSTICIA GRATUITA**

    Propósito: Asistencia Justicia Gratuita (Gob)

- **LIBROS DE REGISTRO**

    Propósito: Certificados, Resoluciones y Órdenes

- **LIMPIEZA METADATOS**

    Propósito: Plataforma de limpieza de Metadatos Incluye servicio web
    LIMPIEZA DE METADATOS WS

- **NÓMINA**

    Propósito: Nómina Corporativa

- **NOTICIAS**

    Propósito: Aplicación de Gestión de Noticias

- **OTRS**

    Propósito: Gestión de Incidencias e ITSM

- **PÁGINAS BLANCAS**

    Propósito: Páginas Blancas

- **PARQUE MÓVIL**

    Propósito: Servicio de Transporte Compartido

- **PEFAC**

    Propósito: Facturas Electrónicas de la Comunidad

- **PERFIL DEL CONTRATANTE**

    Propósito: Perfil del Contratante

- **PLATEA**

    Propósito: Gestión de Expedientes Incluye MODELA / TRAMITA y Gestor

- **MAyTE**

    Propósito: Gestor de expedientes MAYTE

- **PLATINO**

    Propósito: Plataforma de Interoperabilidad

- **PLYCA**

    Propósito: Sistema de Licitación y Compras Electrónicas

- **PORTAFIRMAS**

    Propósito: Aplicación de Portafirmas

- **REGECON**

    Propósito: Registro de la actividad convencional

- **RESERVA DE SALAS**

    Propósito: Reserva de salas de multiconferencia

- **SEFLOGIC**

    Propósito: Sistema Económico-Financiero y Logístico de Canarias

- **SICAC**

    Propósito: Sistema de Información Administrativa del Gobierno de
    Canarias

- **SICHO**

    Propósito: Sistema de control de horario

- **SIMED**

    Propósito: Sistema de Inspección Médica

- **SIRHUS**

    Propósito: Sistema de Información de RRHH

- **SIRVETE**

    Propósito: Sistema de Peticiones/Incidencias

- **eSPERIA**

    Propósito: Gestión de Archivos Documental Incluye servicio web
    eSperia

- **TRASOS**

    Propósito: Tramitación Telemática de Solicitudes Incluye
    Solicitudes, Gestión y Administración

## ESC - Estimación Subjetiva de Calidad

### Carácteristicas deseables de una estimación

- **Comparables**: Los resultados deberían poderse comparar, tanto entre
  diferentes sistemas de información, como respecto al mismo sistema de
  información en distintos momentos del tiempo.

- **Transparencia**: Todo el mundo debería ser capaz de comprender como
  se calcula el indicador, y ser capaz de comprobar los cálculos
  realizados.

- **Monotonicidad**: La función de cálculo del indicador debería ser
  monótona con respecto a la calidad del sistema. Es decir, una mejora
  en la calidad del sistema debería reflejarse en un incremento del
  indicador, y viceversa.

### Propuesto de función de cálculo del IDS

- Un número en un intervalo definido. Se sugiere **entre 0 y 100**,
  siendo 0 la nota más baja y 100 la nota más alta.

- Los 100 puntos se distribuyen en **dimensiones** o **áreas**. Se
  sugieren estas 5 áreas:

    - Seguridad
	
    - Reutilización e Interoperabilidad
	
    - Personas
	
    - Calidad
	
    - Protección de datos
	
    Nota: Quiza se podrían unificar seguridad y protección de datos en
    una sola, lo que nos dejaría solo cuatro áreas.
	
    El peso de cada área *puede* ser diferente, pero la suma total debe
    ser siempre la puntuación total (100 es la propuesta). Lo más
    sencillo sería asignar 20 puntos a cada área (25 si se unifican las
    áreas de Seguridad y Protección de datos)
	
- Cada pregunta dentro de un área se pondera en el intervalo [0..1].  Se
  calcula el total de cada área de la forma:

        $T_a = P_a \dot \sum_{i=1}^{n} P_i$
	
  Donde:

    - $T_a$ es la estimación del área
    - $P_a$ es el peso total del área	(20 en la propuesta)
    - $n$ es el número total de preguntas en el área
    - $P_i$ es el peso de la i-esima pregunta del área
	
  Y el valor final ESC (Estimación Subjetiva de la Calidad) es:

    - $ESC = T_a + T_i + T_p + T_{cd} + T_{pd}$
	
  Donde:

  - $T_a$ es la estimación en la dimensión de seguridad
  - $T_i$ es la estimación en la dimensión de interoperabilidad
  - $T_p$ es la estimación en la dimensión de personas
  - $T_{cd}$ es la estimación en la dimensión de calidad de datos
  - $T_{pd}$ es la estimación en la dimensión de protección de datos
