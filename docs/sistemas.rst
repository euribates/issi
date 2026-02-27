************************************************************************
Sistemas
************************************************************************

.. graphviz:: images/sistemas.dot

Requisitos de calidad de los sistemas
------------------------------------------------------------------------

El sistema define tres niveles de calidad, en lo que respecta a los datos
amacenados para cada sistema:

- **Calidad Mínima**

    Como mínimo, los datos del sistema cumplen las siguientes reglas de
    validación / aceptación:

    - El sistema debe **tener un nombre**, y este debe ser **único**. La longitud
      máxima del nombre es de 220 caracteres. 

    - El sistema debe **tener un código de identificación** del sistema, también
      **único**. Además, el código tiene que estar compuesto
      únicamente por letras mayúsculas, dígitos y el carácter subrayado
      (``_``). La longitud máxima del código identificativo es de 32
      caracteres.

  Si un sistema solo contiene estos datos (que son el mínimo estrictamente
  necesario para dar de alta el sistema), se considera que el sistema
  esta **Pendiente de algunos datos críticos**. El icono de
  estado se mostrara en rojo.

- **Incompleto**

  Se considera un sistema como incompleto si presenta alguna de las
  siguientes deficiencias:

    - Falta el campo **Finalidad**.

    - Falta el campo **Descripción**.

    - El sistema no está vinculado a una **unidad organizativa**.

    - El sistema no tiene asignada una **materia competencial**.

    - El sistema no ha sido asignado a una **familia**, o no se ha marcado
      como no encuadrable en el sistema de familias.

    - No tiene asignada ninguna persona como responsable técnico o
      funcional (Es decir, que tiene que tener al menos una persona
      asignada como responsable de cualquier tipo).

  Posibilidades **a considerar**:

      - Podemos fortalecer la condición relativa a las personas
        responsable, exigiendo que tiene que haber
        al menos un responsable técnico y un responsable funcional,
        obligatoriamente.

      - Se podría incluir que el sistema tenga obligatoriamente
        las respuestas del cuestionario específico.

  Si un sistema no cumple **cualquiera** de estas condiciones,
  se considera que el sistema está
  **pendiente de algunos datos**.
  El icono de estado se mostrará en amarillo.

- **Completo**

  Si el sistema no presenta **ninguda** de las deficiencias del apartado
  anterior, se considera **Completo**. 
  El icono de estado se mostrará en verde.


Modelos
========================================================================

.. automodule:: sistemas.models
   :members: 

Vistas
========================================================================

.. automodule:: sistemas.views
   :members: 
