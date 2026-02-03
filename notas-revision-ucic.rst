.. |UCIC| replace:: Consejería de Universidades, Ciencia e Innovación y Cultura

Notas revisión carga de datos SSI - |UCIC|
========================================================================

Índice

- Líneas marcados como eliminados

- Registro electrónico

- Subvenciones

- Resto de entradas

Líneas marcados como eliminados
------------------------------------------------------------------------

Las entradas desde el índice **374 hasta el 417**, ambas inclusivo, se
han marcado como borradas.  No está claro como han llegado ahí, pero no
parecen ser descripciones de sistemas, sino una seria de indicadores
estadísticos (por ejemplo: Número total de actuaciones de Artes
Escénicas y Música). No tienen ni finalidad, ni responsables
tecnológicos ni funcionales , ni normativa, ni observaciones.

Se han marcado como borrados, pero ¿quizá no merece la pena mantenerlas,
sino borrarlos físicamente de lo hoja de cálculo? No parecen aportar
absolutamente nada. Y, en caso de ser necesaria esta información, siempre
tenemos las hojas de calculo presentadas originalmente. Un problema de
esto es que cambiará los números de los siguientes registros.


Registro electrónico
------------------------------------------------------------------------

¿Se refiere al registro de entrada/salida?


Subvenciones
------------------------------------------------------------------------

La mayoría de las líneas parecen ser diferentes tipos de subvenciones, la
mayoría además, clasificadas por año (por ejemplo ``GESTIÓN VIRTUAL DE
EXPEDIENTES DE LA CONVOCATORIA DE SUBVENCIÓN DIGINNOVA 2025``).
Los registros son los numerados desde el 257 hasta el 362.

Posibles formas de abordar este problema:

- Crear un solo sistema, p.e. ``SUBVENCIONES_UNIVERSIDADES``. Aplazar el
  tratamiento de toda esta complejidad cuando lleguemos a la fase de
  análisis de los datos, tratar cada tipo de subvención como una fuente de
  datos diferente. Sustituimos estas 106 entradas por una sola.

- Crear un sistema principal, y crear cada tipo de subvención (obviando
  los años) como un subsistema. Con esta pasamos de las 106 entradas a
  unas 35, quizá menos porque hay algunas que podrían ser duplicados. No
  está muy claro que esto nos aporte mucha información, a no ser que en la
  realidad, cada tipo de subvención se lleve por equipos diferentes y sin
  relación entre si. En ese caso, se podría asignar de forma única
  responsables tecnológicos o funcionales, áreas temáticas y/o normativa
  especifica para cada tipo.


Tipos de subvenciones detectadas:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

- ``APCR`` (284, 294)
- ``APORTACIONES DINERARIAS`` (362)
- ``AYUDAS POSTDOCTORALES PROGRAMA CATALINA RUIZ`` (303)
- ``BONOS DIGITALES`` (267, 279)
- ``BONOS INNOVACION`` (290, 308, 320)
- ``BONOS TRANSFORMACION DIGITAL`` (309)
- ``CLUSTER`` (258, 263, 286, 300, 307, 317)
- ``COMPETENCIA DIGITAL`` (310, 325, 332, 339)
- ``COMPETENCIAS DIGITALES`` (291, 321)
- ``CPI`` (281)
- ``DIGINNOVA`` (268, 269)
- ``EATIC`` (274, 299, 306, 323, 329, 334, 340)
- ``EPIRIS`` (257)
- ``ESTANCIAS`` (265, 288, 293, 301, 324, 333, 338, 346, 358, 359)
- ``EXPRESIONES DE INTERES`` (272)
- ``FM`` (314)
- ``GESIN`` (287)
- ``GESTORES DE INNOVACION`` (298, 305)
- ``ICCID`` (352)
- ``ICT`` (280)
- ``IMPULSO DE PROYECTOS INNOVADORES`` (275, 289)
- ``INNOBONOS`` (273, 328)
- ``IPROIC`` (262)
- ``PEIS`` (296)
- ``PRESTAMOS`` (357)
- ``PRESTAMOS DIRECTOS`` (361)
- ``PROIS`` Proyectos de Innovación Social (264, 277, 283)
- ``PROYECTOS I+D`` (260, 270, 302, 322, 344)
- ``REDCIDE``, o ``RED CIDE`` (259, 271, 316, 336, 341, 350, 351, 356)
- ``REPT`` (354)
- ``SCAIE`` (353)
- ``SUBVENCION DIRECTA`` (360)
- ``TDT`` (313)
- ``TESIS`` (266, 278, 282, 295, 311, 315, 330, 335, 342, 348, 349, 355)
- ``TECNOLOGOS``, o ``TECNÓLOGOS`` (261, 276, 285, 297, 304, 319, 327, 343)


Dudas:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

- ¿Son las ``APCR`` lo mismo que las ``AYUDAS POSTDOCTORALES PROGRAMA
  CATALINA RUIZ``?

- ¿Es ``COMPETENCIA DIGITAL`` lo mismo que ``COMPETENCIAS DIGITALES``?

- ¿Es ``GESIN`` lo mismo que ``GESTORES DE INNOVACION``?

- ¿Es ``INNOBONOS`` lo mismo que BONOS ``INNOVACION``?

- ¿Una excepción podría ser el de Ayudas o prestamos directos? Puede que
  el proceso para estas ayudas sea demasiado diferente del de las ayudas y
  subvenciones normales.

Asumimos que:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

- ``REDCIDE`` es lo mismo que ``RED CIDE``

- ``TECNOLOGOS`` es lo mismo que ``TECNÓLOGOS``


Resto de entradas
------------------------------------------------------------------------

Hay varias entradas identificables como ``AED`` y ``AED2``:

- ``Aplicaciones AED Centos 7``
- ``OFICINA AED2 PROCEDIMIENTOS``
- ``OFICINA AED2 TIPOS DOCUMENTOS``
- ``OFICINA AED2 USUARIOS``
- ``OFICINA AED2 AED``
- ``Aplicaciones AED RedHat 9``
- ``AED FAP CONO - PROCEDIMIENTOS``
- ``AED FAP CONO-TIPOS DOCUMENTOS``
- ``AED FAP CONOCIMIENTO- USUARIOS``
- ``AED FAP CONOCIMIENTO - AED``

Hay que ver si lo tratamos como un solo sistema, dos, o diez. Para ello
necesitamos más información, especialmente el propósito. Parece ser un
gestor de expedientes.

El resto de entradas, parece completo, aunque se podría profundizar un
poco más en la finalidad o propósito:

- ``Agenda Cultural de Canarias (eventos, actividades y exposiciones)``
- ``a3CON``
- ``PROGRESS PODIO``
- ``Base de datos Bienes insulares``
- ``Base de datos Bienes Muebles``
- ``Fondo Documental``
- ``Inventario Arquitectónico``
- ``Sistema Integrado de Gestión Bibliotecaria``

