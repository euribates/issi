#!/usr/bin/env python3

from comun.error import errors


@errors.register
class EI0001:
    name = "Número incorrecto de columnas"
    desc = (
        "El fichero CSV solo puede tener"
        " 9 columnas o 10 columnas" 
        "pero tiene {value}."
        )
    refs = [
        'importacion_inicial',
        'importacion_adicional'
        ]

@errors.register
class EI0002:
    name = "Código Identificador Interno incorrecto"
    desc = (
        "El valor indicado en el CII no sigue las reglas de "
        "formato esperadas. Solo son válidos los caracteres "
        "desde la ``A`` hasta la ``Z``, sin minúsculas, los "
        "dígitos desde el cero hasta el nueve, y el caracter "
        "subrayado.\n"
        "Además, no puede empezar por un dígito, y debe "
        "tener tres o más caracteres. El valor indicado "
        "{value} no sigue el formato."
        )
    refs = ['Codigo Identificador Interno <CII>']


@errors.register
class EI0003:
    name = "Falta el Código Identificador Interno"
    desc = "El código de Identificación interno es obligatorio."


@errors.register
class I0004:
    name = "Código identificador interno duplicado"
    desc = (
        "Se está intentado dar de alta un sistema de información"
        " con un código identificador interno que coincide con el"
        " de otro ya creado: {value}."
        )


@errors.register
class EI0005:
    name = "Codigo UUID incorrecto"
    desc = (
        "El valor indicado como código UUID: {value}"
        " no sigue las reglas de formato esperadas."
        )
    refs = ['Formato UUID <formato_uuid>']


@errors.register
class EI0006:
    name = "El código o nombre del tema es incorrecto"
    desc = "Los valores esperados están en la tabla de materias."
    refs = ['materias competenciales <materias_competenciales>']


@errors.register
class EI0007:
    name = "Código DIR3 incorrecto o desconocido"
    desc = "El DIR3 indicado: {value} no parece correcto."


@errors.register
class EI0008:
    name = "Materia competencial desconocida o incorrecta"
    desc = (
        "Los valores esperados están en la tabla de materias,"
        " pero {value} no está entre ellos."
        )
    refs = ['materias competenciales <materias_competenciales>']


@errors.register
class EI0009:
    name = "Email o login de usuario incorrecto"
    desc = (
        "No puedo interpretar {value} como un *email* o un login"
        " de usuario."
        )


@errors.register
class EI0010:
    name = "UUID no identificado"
    desc = (
        'Se ha indicado un UUID de sistema: {value}'
        ' que no existe en la base de datos.'
        )
    refs = ['Formato UUID <formato_uuid>']


@errors.register
class EI0011:
    name = "Código duplicado"
    desc = (
        'Ya existe en la base de datos'
        ' un sistema con el codigo indicado: {value}.'
        )
