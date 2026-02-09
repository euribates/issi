#!/usr/bin/env python3

from html import escape
from dataclasses import dataclass


@dataclass
class ErrorMessage():

    code: str
    name: str
    message: str
    context: dict

    def __str__(self) -> str:
        '''Descripción del error en texto plano.
        '''
        buff = [f'Error {self.code}: {self.name} ']
        buff.append(self.message)
        if self.context:
            for _name, _val in self.context.items():
                buff.append(f' - {_name}: {escape(repr(_val))}')
        return '\n'.join(buff)

    def as_html(self):
        '''Descripción del error en formato HTML.
        '''
        buff = [
            '<div class="error-message">',
            '<p>',
            f'<code class="codigo-error">{self.code}</code>:'
            f' <b class="nombre-error">{self.name}<b>.',
            f'{self.message}',
            '</p>',
            ]
        if self.context:
            buff.append('<dl>')
            for _name, _val in self.context.items():
                buff.append(f'<dt>{_name}</dt>')
                buff.append(f' <dd>{escape(repr(_val))}</dd>')
            buff.append('</dl>')
        buff.append('</div>')
        return '\n'.join(buff)

    def __call__(self, value=None, **context):
        message = self.message
        if value:
            message = message.format(value=escape(repr(value)))
        return ErrorMessage(
            self.code,
            self.name,
            message,
            context.copy(),
            )


class ErrorCatalog:

    def __init__(self):
        self.kernel = {}

    def register(self, code, name, desc='', refs=None):
        '''Decorador para registar una clase de error en el catálogo.
        '''
        refs = list(refs) if refs else []
        self.kernel[code] = ErrorMessage(code, name, desc, refs)

    def __len__(self):
        return len(self.kernel)

    def __getattr__(self, name):
        if name in self.kernel:
            return self.kernel[name]
        raise AttributeError(
            'La clase ErrorCatalog no tienen ningún'
            f' atributo llamado {escape(name)}'
            )

    def __getitem__(self, key):
        return self.kernel[key]

    def __iter__(self):
        return iter(list(self.kernel.items()))

    def keys(self):
        '''Devuelve los códigos de errores registrados.
        '''
        return self.kernel.keys()


errors = ErrorCatalog()


errors.register(
    'EI0001',
    "Número incorrecto de columnas",
    desc=(
        "El fichero CSV solo puede tener"
        " 9 columnas o 10 columnas" 
        "pero tiene {value}."
        ),
    refs=['importacion_inicial', 'importacion_adicional'],
    )


errors.register(
    'EI0002',
    "Código Identificador Interno incorrecto",
    desc=(
        "El valor indicado en el CII no sigue las reglas de "
        "formato esperadas. Solo son válidos los caracteres "
        "desde la `A` hasta la `Z`, sin minúsculas, los "
        "dígitos desde el cero hasta el nueve, y el caracter "
        "subrayado.\n"
        "Además, no puede empezar por un dígito, y debe "
        "tener tres o más caracteres. El valor indicado: "
        "«{value}» no sigue el formato."
        ),
    refs=['Codigo Identificador Interno <CII>']
    )


errors.register(
    'EI0003',
    "Falta el Código Identificador Interno",
    desc="El código de Identificación interno es obligatorio.",
    )

errors.register(
    'EI0004',
    "Código identificador interno duplicado",
    desc=(
        "Se está intentado dar de alta un sistema de información"
        " con un código identificador interno que coincide con el"
        " de otro ya creado: {value}."
        )
    )

errors.register(
    'EI0005',
    "Codigo UUID incorrecto",
    desc=(
        "El valor indicado como código UUID: {value}"
        " no sigue las reglas de formato esperadas."
        ),
    refs=['Formato UUID <formato_uuid>'],
    )

errors.register(
    'EI0006',
    "El código o nombre del tema es incorrecto",
    desc="Los valores esperados están en la tabla de materias.",
    refs=['materias competenciales <materias_competenciales>'],
    )

errors.register(
    'EI0007',
    "Código DIR3 incorrecto o desconocido",
    desc="El DIR3 indicado: {value} no parece correcto.",
    )

errors.register(
    'EI0008',
    "Materia competencial desconocida o incorrecta",
    desc=(
        "Los valores esperados **no** están en la tabla de materias,"
        " pero «{value}» no está entre ellos."
        ),
    refs=['materias competenciales <materias_competenciales>'],
    )


errors.register(
    'EI0009',
    "Email o login de usuario incorrecto",
    desc=(
        "No puedo interpretar «{value}» como un *email"
        " o un login de usuario."
        ),
    )


errors.register(
    'EI0010',
    "UUID no identificado",
    desc=(
        'Se ha indicado un UUID de sistema: «{value}»'
        ' que no existe en la base de datos.'
        ),
    )


errors.register(
    'EI0011',
    "Código duplicado",
    desc=(
        'Ya existe en la base de datos'
        ' un sistema con el codigo indicado: {value}.'
        ),
    )


errors.register(
    'EI0012',
    "Código de Juriscán no reconocido",
    desc=(
        'No es posible conseguir la información de Juriscán'
        ' para la clave suministrada: {value}.'
        ' Se esperaba o bién una serie de digitos o una'
        ' URL con el patrón:\n\n'
        ' gobiernodecanarias.org/juriscan/ficha.jsp?id=<cod. jur.>.\n\n'
        ' Es posible que el código esté mal o que la conexión'
        ' con Juriscán esté caida en este momento.'
        ),
    )


errors.register(
    'EI0013',
    "Falta el nombre del sistema",
    desc=(
        "El nombre del sistema es obligatorio, y tiene que tener"
        " como mínimo 3 caracteres. {value} no es un nombre válido"
        ),
    )
