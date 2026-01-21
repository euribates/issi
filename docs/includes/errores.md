- `EI0001`: **Número incorrecto de columnas**.
  El fichero CSV solo puede tener 9 columnas o 10 columnaspero tiene
  **VALUE**.
  Véase:

    - {ref}`importacion_inicial`.
    - {ref}`importacion_adicional`.

- `EI0002`: **Código Identificador Interno incorrecto**.
  El valor indicado en el CII no sigue las reglas de formato esperadas.
  Solo son válidos los caracteres desde la `A` hasta la `Z`, sin
  minúsculas, los dígitos desde el cero hasta el nueve, y el caracter
  subrayado. Además, no puede empezar por un dígito, y debe tener tres
  o más caracteres. El valor indicado: «**VALUE**» no sigue el
  formato.
  Véase:

    - {ref}`Codigo Identificador Interno <CII>`.

- `EI0003`: **Falta el Código Identificador Interno**.
  El código de Identificación interno es obligatorio.

- `EI0004`: **Código identificador interno duplicado**.
  Se está intentado dar de alta un sistema de información con un código
  identificador interno que coincide con el de otro ya creado:
  **VALUE**.

- `EI0005`: **Codigo UUID incorrecto**.
  El valor indicado como código UUID: **VALUE** no sigue las reglas de
  formato esperadas.
  Véase:

    - {ref}`Formato UUID <formato_uuid>`.

- `EI0006`: **El código o nombre del tema es incorrecto**.
  Los valores esperados están en la tabla de materias.
  Véase:

    - {ref}`materias competenciales <materias_competenciales>`.

- `EI0007`: **Código DIR3 incorrecto o desconocido**.
  El DIR3 indicado: **VALUE** no parece correcto.

- `EI0008`: **Materia competencial desconocida o incorrecta**.
  Los valores esperados **no** están en la tabla de materias, pero
  «**VALUE**» no está entre ellos.
  Véase:

    - {ref}`materias competenciales <materias_competenciales>`.

- `EI0009`: **Email o login de usuario incorrecto**.
  No puedo interpretar «**VALUE**» como un *email* o un login de
  usuario.

- `EI0010`: **UUID no identificado**.
  Se ha indicado un UUID de sistema: «**VALUE**» que no existe en la
  base de datos.
  Véase:

    - {ref}`Formato UUID <formato_uuid>`.

- `EI0011`: **Código duplicado**.
  Ya existe en la base de datos un sistema con el codigo indicado:
  **VALUE**.

