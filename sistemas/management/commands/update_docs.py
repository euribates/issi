#!/usr/bin/env python3

import textwrap

from django.core.management.base import BaseCommand
from django.core.management import CommandError

from sistemas.models import Tema
from sistemas.models import Ente


CMD_NAME = 'update_docs'
ABOUT    = 'Actualizar los ficheros de actualización'
EPILOG   = 'ISSI - Inventario de sistemas de información'

PARTES = [
    'materias',
    'entes',
    'errores',
    'glosario',
    ]


def wrap(texto: str, width=75, indent='  ') -> str:
    return '\n'.join(textwrap.wrap(
        texto, 
        subsequent_indent=indent,
        ))


def print_errores():
    '''Imprime los errores registrados en el sistema.

    En formato RestructuredText.
    '''
    from sistemas.error import errors
    for code, err in errors:
        desc = err.desc.format(value="**VALUE**")
        print(f'- ``{code}``: **{err.name}**.')
        print(f'  {wrap(desc)}')
        if err.refs:
            print('  Véase:\n')
            for _ref in err.refs:
                print(f'    - :ref:`{_ref}`.')
        print()


def print_glosario():
    """Imprime el glosario en formato docutils.
    """
    from glosario.models import Termino
    print('# Glosario de términos')
    print()
    print('```{glossary}')
    print(':sorted:')
    for termino in Termino.objects.all():
        print()
        print(f'{termino.entrada}')
        for paragraph in termino.descripcion.split('\n'):
            paragraph = paragraph.strip()
            if paragraph:
                print('\n'.join(textwrap.wrap(
                    paragraph,
                    initial_indent='\n    ',
                    subsequent_indent='    ',
                    )))
            first_indent = '\n    '
class Command(BaseCommand):
    help = ABOUT

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('parte', choices=PARTES)

    def handle(self, *args, **options):
        """Punto de entrada.
        """
        parte = options.get('parte')
        match parte:
            case 'materias':
                print('======= =========================================')
                print('Código  Materia competencial')
                print('======= =========================================')
                for tema in Tema.objects.all():
                    print(f'``{tema.pk}`` {tema.nombre_tema}')
                print('======= =========================================')
            case 'entes':
                print('============= =========================================')
                print('Cód. Ente     Nombre del organismo o dirección general')
                print('============= =========================================')
                for ente in Ente.objects.all():
                    codigo = f'``{ente.pk}``' 
                    print(f'{codigo:13} {ente.organismo.nombre_organismo}')
                print('============= =========================================')
            case 'errores':
                print_errores()
            case 'glosario':
                print_glosario()
            case _:
                raise CommandError(
                    f'No se como generar el fragmento {parte}'
                    )
