#!/usr/bin/env python3

import argparse

from django.core.management.base import BaseCommand

ABOUT    = 'Crea la tabla de frecuencias a partir del fichero spanish.txt'
EPILOG   = 'ISSI - Inventario de sistemas de información'


class Command(BaseCommand):
    '''Generación de la tabla de frecuencias.
    '''
    help = ABOUT

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)
    
    def handle(self, *args, **options):
        count = 0
        with open('spanish.txt', 'r') as f_in:
            for line in f_in:
                for c in line:
                    if c == 'w':
                        count += 1
                        print(line, end=' ')
        print(count)
