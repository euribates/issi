Descripción de activos de datos
========================================================================

Para cada activo de dato, se describen los siguientes valores:


==============================  =======================================
Nombre (subtipo)                Descripción
==============================  =======================================
id_activo (``int/pk``)          Clave primaria del activo.
sistema (``int/fk``)            Clave foránea del sistema de
                                información.
nombre_activo (``str/name``)    Nombre del activo.
descripcion (``str``)           Descripción del activo.
es_prioritario (``bool``)       El activo es de importancia alta
georeferenciado (``bool``)      El activo está georeferenciado
datos_personales (``str/fk``)   Nivel de protección de los datos
                                del activo. Los valores posibles
                                Puede ser:
                                  - No contiene datos personales
                                  - Contiene datos personales
                                  - Contiene datos personales
                                    especialmente sensibles
f_alta (``datetime/create``)    Fecha de alta.
f_cambio (``datetime/update``)  Fecha última modificación.
f_baja (``datetime/archive``)   Fecha baja lógica / atchivado.
==============================  =======================================


Notas de diseño:
------------------------------------------------------------------------

- El subtipo no se refiere a una especialización del tipo, en el sentido
  de, pongamos ``int64`` para indicar un entero de 64 bits, sino que
  trabaja a un nivel semántico. En otras palabras, no intenta
  especificar como se almacena sino para qué se usa ese valor. La
  definición concreta de la representación, como ``int64`` está definida
  en el propio esquema de la base de datos y no hace falta almacenarla.

- No hay que tener infinitos subtipos. Si no se puede clasificar
  un entero, por ejemplo, en ninguno de los casos de usos
  incluidos, se usa solo ``int``.

- Se pueden incluir nuevo tipos / usos, bajo demanda

- Quizá más que subtipo, deberíamos llamarlo ``uso`` o ``usage``?


Tipos y casos de uso
------------------------------------------------------------------------

Cadenas de texto (``str``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``str/name``  

  Nombre (En general). Para nombres de personas, mejor
  usar ``str/person/name`` y ``str/person/surname``.

- ``str/person/name``

  Nombre (de persona)

- ``str/person/surname``

  Apellidos (de persona)

- ``str/email``

  Dirección de correo electrónico

- ``str/url``

  Dirección página web. Debe empezar por ``http://`` o ``https://``.


Números enteros (``int``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``int/pk``

  Clave primaria. Identificador único de un recurso

- ``int/fk``    

  Clave foránea. Un valor de la clave primaria de otra tabla, almacenada
  en esta. Es el mecanismo usado en bases de datos relacionales para
  almacenar relaciones de 1 a N o de N a N.

- ``int/counter``

  Contador. Si se refiere a contar el número de elementos en un sistema
  de almacenaje, se recomienda usar ``int/stock``.

- ``int/index``

  Índice

- ``int/stock``

  Cantidad de elementos en un inventario

- ``int/seconds``

  Cantidad de tiempo, en segundos

- ``int/minutes``

  Cantidad de tiempo, en minutos

- ``int/hours``

  Cantidad de tiempo, en horas

- ``int/days``

  Cantidad de tiempo, en días

- ``int/currency/eur``    Importe, en euros.
    
.. note:: 

    Los códigos para cada moneda y sus subunidades, si las hubiera,
    están sacados de la `ISO 4217`_.

- ``int/currency/eur_subunit``

  Importe monetario, en céntimos de euro. Un euro (``int/currency/eur``)
  equivale a 100 céntimos (``int/currency/eur_subunit)


- ``int/currency/usd`` 

  Importe monetario, en dolares norteamericanos

- ``int/currency/usd_subunit``

  Importe monetario, en céntimos de dolar. Un dolar
  norteamericano (``int/currency/usd``) equivale a 100 céntimos
  (``int/currency/usd_subunit``)


- ``int/currency/gbp``

  Importe monetario, en libras esterlinas

- ``int/currency/gbp_subunit``

  Importe monetario, en peniques de libras esterlinas. Una
  libra (``int/currency/gbp``) equivale a 100 peniques 
  (``int/currency/gbp_subunit``)


Número decimales o en coma flotante (``float``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``float/currency/eur``

  Importe monetario, en euros, con decimales
    
- ``float/currency/usd``

  Importe monetario, en dolares norteamericanos, con decimales

- ``float/currency/gbp``

  Importe monetario, en libras esterlinas, con decimales

- ``float/geo/lat``

  Latitud geográfica, en grados.

- ``float/geo/long``

  Longitud geográfica, en grados.


Fechas (``date``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``date/person/birdhdate``

  Fecha de nacimiento

- ``date/start``

  Fecha de inicio de plazo. No se especifica la hora.  En principio,
  se considera que el plazo empieza a las 00:00:00. Si hiciera
  falta especificar la hora se recomienda usar ``datetime/start``.

- ``date/end``        

Fecha de fin de plazo. No se especifica la hora, por lo que se entiende
que el plazo termina a las 23:50:59. Si hiciera falta especificar la
hora se recomienda usar `datetime/end`

- ``date/archived``   

Fecha en la que se archivó o se realizó el borrado lógico de algún activo de datos.


Fechas y horas (``datetime``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un valor que almacena a la vez una Fecha y hora. Se representará, si se
puede, como tipo de datos nativo, y preferentemente se almacenará
incluyendo la marca de zona temporal. En caso de no poder usar un tipo
de datos nativo, se recomienda para su almacenamiento y/o intercambio
representarla en forma de texto usando el formato `ISO 8601`_.

Para Canarias, el identificador de zona es ``Atlantic/Canary``, y se
siguen el huso horario de Europa occidental, ``UTC+0`` (``WET``) en
invierno y ``UTC+1`` (``WEST``) en verano. El cambio a horario de verano
ocurre a las ``01:00`` de la madrugada, el último domingo de marzo,
cuando los relojes adelantan una hora, y el último domingo de octubre,
donde se atrasan (Ver Directiva `2000/84/CE`_ del Parlamento Europeo Y
del consejo de 19 de enero de 2001, relativa a las disposiciones sobre
la hora de verano).


- ``datetime/person/birdhdate``

  Fecha y hora de nacimiento.

- ``datetime/start``

  Fecha y hora de inicio de plazo.

- ``datetime/end``

  Fecha y hora de fin de plazo

- ``datetime/created``

  Fecha y hora de creación de un recurso

- ``datetime/updated``

  Fecha y hora de modificación de un recurso
  
- ``datetime/archived`` 

  Fecha y hora de borrado lógico o archivado de un recurso. Para
  borrados físicos es preferible usar ``datetime/deleted``.

- ``datetime/deleted``

  Fecha y hora de borrado físico de un activo. Para un borrado lógico es
  preferible usar ``datetime/archive``.


Valores lógicos (``bool``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los valores booleanos se representará en la base de datos como tipo
booleano nativo, si la base de datos y el lenguaje lo permiten. Si no
lo permite, se recomienda usar un entero de 1 byte, restringido sus
valores posibles a ``0`` y ``1``. Cualquier otro valor debe rechazarse
y producir el error.


- ``bool/auth``

  Autorización o permiso. Verdadero si está autorizado, falso en caso
  contrario

- ``bool/forbbiden``

  Prohibición. Verdadero si está prohibido, falso en caso contrario

- ``bool/active``

  Marca de activo. El valor verdadero indica que el recurso está activo

- ``bool/inactive``

  Marca de recurso inactivo. El valor verdadero indica que el recurso
  está inactivo




.. _ISO 8601: https://es.wikipedia.org/wiki/ISO_8601
.. _ISO 4217: https://es.wikipedia.org/wiki/ISO_4217
.. _2000/84/CE: https://www.boe.es/doue/2001/031/L00021-00022.pdf
