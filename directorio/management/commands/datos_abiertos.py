#!/usr/bin/env python3


import colorama
from django.conf import settings
from django.core.management.base import BaseCommand

from directorio import models


CMD_NAME   = 'datos_abiertos'
ABOUT      = 'Obtiene el conjunto de datos abiertos publicados por un organismo'
EPILOG     = 'ISSI - Inventario de sistemas de información'

HOST       = 'datos.canarias.es'
CATALOGO   = f'catalogos/general/organization'
SLUG       = 'presidencia-del-gobierno'

VALID_DAYS = 15

RED       = colorama.Fore.RED
YELLOW    = colorama.Fore.YELLOW
BRIGHT    = colorama.Style.BRIGHT
GREEN     = colorama.Fore.GREEN
RESET_ALL = colorama.Style.RESET_ALL


class Command(BaseCommand):

    help = ABOUT

    def __init__(self, *args, **kwargs):
        colorama.just_fix_windows_console()
        super().__init__(*args, **kwargs)

    def warning(self, msg: str):
        '''Mensaje de aviso.
        '''
        self.stdout.write(
            f'{YELLOW}Atención{RESET_ALL} {BRIGHT}{msg}{RESET_ALL}'
            )
        
    def success(self, msg: str):
        '''Mensaje de éxito.
        '''
        self.stdout.write(
            f'{GREEN}OK{RESET_ALL}: {BRIGHT}{msg}{RESET_ALL}'
            )

    def panic(self, msg: str):
        '''Mensaje de error crítico.
        '''
        self.stderr.write(
            f'{RED}Error{RESET_ALL}: {BRIGHT}{msg}{RESET_ALL}'
            )


    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--force',
            action='store_true',
            help='Forzar la descarga',
            default=False,
            )
        parser.add_argument(
            '-i', '--id',
            help='Identificador DIRCAC',
            type=int,
            )
        parser.add_argument(
            '-d', '--dir3',
            help='Identificador DIR3',
            )
    
    def selecciona_organismo(self, options):
        id_dircac = options.get('id')
        if id_dircac:
            return models.Organismo.load_organismo(id_dircac)
        dir3 = options.get('dir3')
        if dir3:
            return models.Organismo.load_organismo_using_dir3(dir3)
        return None

    def handle(self, *args, **options):
        organismo = self.selecciona_organismo(options)
        if not organismo:
            self.panic('no se ha especificado el organismo')
            return
        if organismo.ente:
            counter = 0
            for desc, url in organismo.ente.get_open_data():
                print(desc, url, sep='\n', end='\n\n')
                counter += 1
            return self.success(
                f'Encontradas {counter} fuentes de detos abiertos'
                )
        else:
            self.warning(f'No hay un ente asociado a {organismo}')
