#!/usr/bin/env python3

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from sistemas import parsers

INPUT_DIR = settings.BASE_DIR / 'imports'

CMD_NAME = 'import_csv'
ABOUT    = 'Importa la hoja de datos de un ente'
EPILOG   = 'ISSI - Inventario de sistemas de información'


LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
END = "\033[0m"


def green(text: str) -> str:
    '''Devuelve el texto en verde.
    '''
    return f'{LIGHT_GREEN}{text}{END}'


def red(text: str) -> str:
    '''Devuelve el texto en rojo.
    '''
    return f'{LIGHT_RED}{text}{END}'


def bold(text: str) -> str:
    return f'{BOLD}{text}{END}'


class Command(BaseCommand):
    help = ABOUT

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def warning(self, msg: str):
        self.console.print(f'[bold][yellow]Atención:[/yellow] {msg}[/bold]')
        
    def success(self, msg: str):
        self.console.print(f'[bold][green]OK:[/green] {msg}[/bold]')

    def panic(self, msg: str):
        self.console.print(f'[bold][red]Error:[/red] {msg}[/bold]')

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            help='Especificar el o los ficheros CSV',
            nargs='+',
            default=None,
            )
        # parser.add_argument(
            # '-v', '--verbose',
            # action='store_true',
            # help='Muestra información adicional',
            # )

    def handle(self, *args, **options):
        verbose = options['verbosity'] > 1
        total_errores = 0
        total_sistemas = 0
        for filename in options['filename']:
            print(f'Comprobando {bold(filename)}:', end='\n' if verbose else' ')
            with open(filename, 'r', encoding="utf-8") as input_file:
                reader = csv.reader(input_file, delimiter=',', quotechar='"')
                _first_line = next(reader)      # Ignoramos la primera fila
                num_errores = 0
                for n_linea, tupla in enumerate(reader, start=1):
                    total_sistemas += 1
                    errors, payload = parsers.parse_row(tupla, n_linea=n_linea)
                    if verbose:
                        print(f'    - {payload["codigo"]}', end=' ')
                        if uuid_sistema := payload.get('uuid_sistema'):
                            print(uuid_sistema, end=' ')
                    if errors:
                        num_errores += len(errors)
                        if verbose:
                            print()
                            for error in errors:
                                print(f'      - Error: {red(error)}')
                    if verbose:
                        if num_errores == 0:
                            print(green('[OK]'))
                        else:
                            print(red(f'[{num_errores} errores]'))
                num_errores = num_errores + len(errors)
                if errors:
                    total_errores += 1
        if verbose:
            if total_errores == 0:
                print('No se ha detectado ningún error')
                print('El fichero está listo para ser importado')
            else:
                print(f'Total errores: {red(total_errores)}')
                print(f'Sistemas váldos: {total_sistemas - total_errores}')
