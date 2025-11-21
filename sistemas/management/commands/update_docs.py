#!/usr/bin/env python3

import csv

from django.core.management.base import BaseCommand
from django.core.management import CommandError

from sistemas.models import Tema
from directorio.models import Ente


CMD_NAME = 'update_docs'
ABOUT    = 'Actualizar los ficheros de actualización'
EPILOG   = 'ISSI - Inventario de sistemas de información'

PARTES = [
    'materias',
    'entes',
    ]

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
            case _:
                raise CommandError(
                    f'No se como generar el fragmento {parte}'
                    )
