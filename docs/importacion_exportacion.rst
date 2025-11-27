************************************************************************
Importación y exportación de los datos
************************************************************************

Estructura del archivo de importación/exportación
========================================================================

En lo que respecta al formato, debe ser un fichero CSV_,
codificado en UTF-8, usando como separador la coma (``,``).

La primera línea debe contener los nombres de los campos, aunque la
importación no comprueba esos valores, es decir, la primera línea
simplemente se ignora.

Para el resto de líneas, los campos de tipo texto deben estar
entrecomillados si contiene caracteres especiales como por ejemplo
saltos de línea, el carácter coma (``,``) o el propio carácter de
comillas (``"``); si no es el caso, pueden ir entre comillas o no
indistintamente.

Cada línea del fichero debe constar de **9 u, opcionalmente 10 campos**.
Esta décima columna adicional, si está presente, contiene un
**identificador único universal**, UUID_ del sistema de información.

En la **carga inicial**, solo se esperan 9 valores por fila.


Campos del fichero CSV
========================================================================

Las columnas del fichero CSV se describen en la siguiente tabla:

==== ==================== ====================================
Ord. Campo (En Fila 1)    Explicación
==== ==================== ====================================
1    Nombre               El nombre del sistema
2    Código Id. Int.      Código identificativo interno
3    Finalidad            Finalidad o propósito del S.I.
4    Materia competencial Código de materia
5    DIR3                 DIR3 Dirección general / organismo
6    Resp. Tecnológico    UserId. de los responsables
7    Resp. Funcional      UserId. de los responsables
8    Normativa            Cód. Juriscán de normativa aplicable
9    Comentarios          Comentarios / sugenrencias
10   UUID (opcional)      Identicador Universal ISSI
==== ==================== ====================================

La décima columna es, como se indica, opcional. El propósito de esta
columna se explica con más detalle en la sección de importación y
exportación de datos. Veremos a continuación el resto de columnas:

- **Nombre**: El nombre oficial del sistema. Se espera una sola palabra
  o una frase corta. Es un **valor único** en la base de datos, así que
  si se intenta dar de alta un sistema con el mismo nombre que otro ya
  existente, se producirá un error y no se producirá ningún efecto
  en la base de datos.

- **Codigo identificativo interno**: Aunque se usa la palabra código, se
  espera aquí una expresión legible, consistente normalmente en el
  nombre, oficial o no, del sistema (por ejemplo, ``PLATINO``. No se
  admiten espacios, ni caracteres especiales, ni vocales acentuadas, ni
  ningún otro símbolo aparte de las letras de la `A` a la `Z`
  (excluyendo la eñe), los dígitos del ``1`` al ``9`` y el carácter
  subrayado, ``_``. Es un **valor único** en la base de datos, así que
  si se intenta dar de alta un sistema con el mismo nombre que otro ya
  existente, se producirá un error y no se producirá ningún efecto en la
  base de datos.

- **Finalidad**: Es un texto breve, de un párrafo, en el que se explica
  la finalidad o propósito del sistema de información. Se admiten varios
  párrafos, separados por saltos de línea (por lo que este campo debería
  ir entrecomillado en el fichero). En caso de incluir más de un
  párrafo, **solo el primero** se almacenará en la base de datos en el
  campo ``finalidad``, el resto del texto se almacenará en el campo
  ``descripcion``. La redacción del texto debería poder leerse como la
  continuación de: ``"El propósito de este sistema de
  información es ..."``.

.. _materias_competenciales:

- **Materia competencial**: Es un código de tres letras, indicando la
  materia competencial a la que está asociado el sistema. Si se
  ignora, dejarlo vacío o con el código especial ``UNK``. La tabla
  de códigos y materias actual es la siguiente:

  .. include:: includes/materias.rst


- **DIR3**: Código DIR3 de la Dirección general u organismo que es
  responsable del mantenimiento funcional y técnico del sistema
  de información. Si no se conoce, dejarlo en blanco.

- **Responsable Tecnológico**: Identificador o identificadores de los responsables
  tecnológicos. Si son varios, vendran separados por comas, lo que
  obliga a que todo el contenido del campo venga entrecomillado. Los
  valores aceptables como identificadores pueden ser de tres tipos:

  - **login** del usuario: Código alfanumérico, normalmente de siete o
    más caracteres. Por ejemplo ``napeape2``.

  - **email** del usuario: El córreo electrónico. Por ejemplo
    ``napeape2@gobiernodecanarias.org``.

  - **Combinación de nombre y correo**: Por ejemplo
    ``Nombre Apellido Apellido2 <napeapr2@gobiernodecanarias.org>``

  Cualquier valor que no se corresponda con los tipos anteriores
  provocará un error e impedirá la carga del archivo. Se recomienda
  incluir al menos a dos responsables técnicos, pero se pueden incluir
  los que se deseen. En caso de no saber o no poder especificar al menos
  uno, dejar el campo en blanco.

- **Responsable Funcional**: Identificador o identificadores de los responsables
  funcionales. Sigue las mismas reglas que para los responsables
  tecnológicos. Igualmente se recomienda incluir al menos dos
  responsables funcionales, si puede ser.

- **Normativa**: Código o códigos Juriscán de la normativa aplicable
  **de forma específica** a este sistema de información. Si no aplica
  o no se conoce, dejarlo en blanco. Si son varios, separarlos por coma; esto obliga a
  entrecomillar todos los valores. Ejemplso válidos: ``74222`` o
  ``"74222, 6732"``.

- **Comentarios**: Campo de texto opcional y libre para comentarios,
  aportaciones, notas de interés, etc. Si contiene más de un párrafo,
  saltos de línea, caracteres especiales, etc. es necesario
  entrecomillarlo.

- **UUID**: Este es un identificados Universal ``UUID``, que se asigna al
  sistema la primera vez que este entra en el inventario. Es opcional en
  la carga inicial de datos ya que, como se explica más adelante, en ese
  caso el sistema lo asigna automáticamente. Si se incluye, es una cadena
  de texto de 36 caracteres. Ejemplo:
  ``29564c1a-4894-473e-85d1-c4c8c60a2333``.


.. _formato_uuid:

.. sidebar:: Formato de un UUID

    Un UUID es un número binario de 128 bits. Su representación textual
    canónica es una cadena de 32 dígitos hexadecimales (base 16)
    mostrados en cinco grupos separados por guiones de la forma
    8-4-4-4-12, dando un total de 36 caracteres (32 caracteres
    alfanuméricos y cuatro guiones).


Importación de datos
========================================================================

Cuando se realice la importación, el tratamiento será diferente según se
utilice un ficheros de 9 columnas o uno de 10. De esta forma
queremos evitar duplicaciones en la base de datos y facilitar la
actualización de los datos.

Si el fichero consta de 9 columnas, se considera una **importación
inicial**, mientras que si usa 10 columnas, se considera una
**importación adicional**.

.. _importacion_inicial:

Importación Inicial
------------------------------------------------------------------------

Como se explicó antes, si se usa el formato de 9 columnas, se considera
que es una **importación inicial**. En este caso, para todos los
sistemas incluidos en el fichero:

- El sistema será **dado de alta**. En términos de base de datos, se
  inserta un nuevo registro.

- Internamente se le **asignará automáticamente** un nuevo
  código ``UUID``, usando la variante ``UUID4``.

Este ``UUID`` será el identificador único asociado ya de forma
permanente con ese sistema.

.. _importacion_adicional:

Importaciones adicionales.
------------------------------------------------------------------------

Si se usa un formato de 10 columnas, se considera que es una
**importación adicional**. Para cada uno de los sistemas incluidos en el
fichero:

- Se usará el valor en la décima columna, es decir, el ``UUID``, para
  verificar si el sistema existe en la base de datos.

- Si no existe, se dará de alta. Esto es, se insertará un nuevo
  registro en la base de datos para este sistema. A diferencia de la
  importación adicional, **no** se asignará automáticamente un ``UUID``
  nuevo, si no que se usará el indicado.

- Si ya existe, es decir, hay un registro en la base de datos que
  coincide con el ``UUID`` indicado, el registro de la base de datos se
  **actualizará** con los valores indicados: Nombre, finalidad, DIR3,
  etc.

Esto permite que las **operaciones de importación adicionales sean
idempotententes**, es decir, podemos importar de forma adicional
varias veces el mismo fichero de importación y el resultado final en la
base de datos será siempre el mismo que si se hubiera subido una sola,
ya que no se crean duplicados.

Obviamente, para que el sistema funcione **nunca debe cambiarse el
código UUID asociado a un sistema de información**, a no ser que sepas
muy bien lo que estás haciendo. Y eso casi nunca pasa. Y lo sabes.


Exportación de datos
========================================================================

La exportación **siempre será de 10 columnas**.


Posibles errores en la importación de datos
========================================================================

Los posibles errores que impiden la carga de datos son los siguientes:

- **Numero incorrecto de columnas**: El fichero CSV solo puede tener
  9 columnas (ver :ref:`importacion_inicial`) o 10 columnas (ver
  :ref:`importacion_adicional`).

- **Código identificativo interno incorrecto**. El valor indicado en el
  CVS no sigue las reglas de formato esperadas.

- **Codigo UUID incorrecto**: El valor indicado como código UUID no sigue
  las reglas de formato esperadas. Ver :ref:`Formato UUID <formato_uuid>`.

- **El código o nombre del tema es incorrecto**: Los valores esperados
  están en la tabla de
  :ref:`materias competenciales <materias_competenciales>`.

- **Código identificativo interno duplicado**: Se está intentado dar de
  alta un sistema de información cuyo código identificativo interno
  coincide con el de otro ya creado. 

.. _CSV: https://es.wikipedia.org/wiki/Valores_separados_por_comas
.. _UUID: https://es.wikipedia.org/wiki/Identificador_%C3%BAnico_universal
