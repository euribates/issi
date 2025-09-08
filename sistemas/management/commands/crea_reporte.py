#!/usr/bin/env python3

import argparse

from django.conf import settings
from django.core.management.base import BaseCommand

CMD_NAME = 'crea_reporte'
ABOUT    = 'Crea un informe indivizualizado por organismo'
EPILOG   = 'ISSI - Inventario de sistemas de información'

DATOS_CANARIAS = 'https://datos.canarias.es/catalogos/general/dataset'
URL_PROCEDIMIENTOS = (
    f'{DATOS_CANARIAS}/946cdcde-2118-48ef-a30a-f9dc812c82db'
    '/resource/10b71b12-fb77-47b7-88f6-ec46ebee1548/download/procedimientos.csv'

PROCEDIMIENTOS = settings.

class Command(BaseCommand):
    help = ABOUT

    def create_parser(self, prog_name, subcommand, **kwargs):
        print('kwargs', kwargs)
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('-s', '--sirhus', help='Identificador SIRHUS', type=int)
        parser.add_argument('-d', '--dir3', help='Identificador DIR3')
    
    def handle(self, *args, **options):
        id_dir3 = options.get('dir3')
        if id_dir3:
            print(f'Generar informe para DIR3 {id_dir3}')
            with open('
        for name, value in options.items():
            print(name, value)




