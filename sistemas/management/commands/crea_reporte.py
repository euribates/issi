#!/usr/bin/env python3

import colorama
from django.core.management.base import BaseCommand

CMD_NAME = 'crea_reporte'
ABOUT    = 'Crea un informe indivizualizado por organismo'
EPILOG   = 'ISSI - Inventario de sistemas de información'

DATOS_CANARIAS = 'https://datos.canarias.es/catalogos/general/dataset'
URL_PROCEDIMIENTOS = (
    f'{DATOS_CANARIAS}/946cdcde-2118-48ef-a30a-f9dc812c82db'
    '/resource/10b71b12-fb77-47b7-88f6-ec46ebee1548/download/procedimientos.csv'
    )

RED = colorama.Fore.RED
RESET_ALL = colorama.Style.RESET_ALL



def warning(msg: str):
    return f'Atención: {RED}{msg}{RESET_ALL}'
    

class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        colorama.just_fix_windows_console()
        super().__init__(*args, **kwargs)

    def create_parser(self, prog_name, subcommand, **kwargs):
        print('kwargs', kwargs)
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('-i', '--id', help='Identificador DIRCAC/SIRHUS', type=int)
        parser.add_argument('-d', '--dir3', help='Identificador DIR3')
    
    def handle(self, *args, **options):
        id_dir3 = options.get('dir3')
        id_dircac = options.get('id')
        if id_dir3:
            print(f'Generar informe para DIR3 {id_dir3}')
            print(warning('Aun por implementar'))
        elif id_dircac:
            print(f'Generar informe para DIRCAC {id_dircac}')
            print(warning('Aun por implementar'))
        else:
            for name, value in options.items():
                print(name, value)
        return 0




