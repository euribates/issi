ESC - Estimación Subjetiva de Calidad
========================================================================

Características deseables de una estimación
------------------------------------------------------------------------

Algunas de las características que deseamos que tenga una estimación de
calidad son las siguientes:

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

Propuesto de función de cálculo del IDS
------------------------------------------------------------------------

- Un número en un intervalo definido. Se sugiere entre 0 y 100, siendo 0
  la nota más baja y 100 la nota más alta.

- Los 100 puntos se distribuyen las siguientes 6 **dimensiones** o **áreas**:

  - Calidad (18 puntos)
  - Interoperabilidad (18 puntos)
  - Personas (10 puntos)
  - Protección de datos (18 puntos)
  - Reutilización (18 puntos)
  - Seguridad (18 puntos)

.. note::

    Quizá se podrían unificar seguridad y protección de datos en una
    sola, hacer lo mismo con reutilización e interoperabilidad, lo que
    nos dejaría solo cuatro áreas.

Cálculo del indicador
------------------------------------------------------------------------

El peso de cada área *puede* ser diferente, pero la suma total debe
ser siempre la puntuación total (100 es la propuesta). 

Cada pregunta dentro de un área se pondera en el intervalo [0..1]. Se
calcula el total de cada área de la forma:

.. math::

    T_a = P_a \frac{\sum_{i=0}^{N} P_i}{N}

Donde:

  - :math:`T_a` es la estimación del área
  - :math:`N` es el número de preguntas en el área  
  - :math:`P_a` es el peso total del área (20 en la propuesta)
  - :math:`p_i` es el peso de la *i-esima* pregunta del área

El valor final ESC (Estimación Subjetiva de la Calidad) es:

$$ ESC = T_c + T_i + T_p + T_d + T_r + T_s $$

Donde:

  - :math:`T_c` es la estimación en la dimensión de calidad
  - :math:`T_i` es la estimación en la dimensión de interoperabilidad
  - :math:`T_p` es la estimación en la dimensión de personas
  - :math:`T_d` es la estimación en la dimensión de protección de datos
  - :math:`T_r` es la estimación en la dimensión de reutilización
  - :math:`T_s` es la estimación en la dimensión de seguridad

  
