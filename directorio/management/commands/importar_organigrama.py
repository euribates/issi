#!/usr/bin/env python3

from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
from pathlib import Path
import csv
from urllib.request import urlretrieve

import colorama
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from django.conf import settings
from filters import clean_text
from filters import clean_integer
from directorio import models


CMD_NAME = 'importar_organigrama'
ABOUT    = 'Crea las tablas de organismos a partir del DIRCAC'
EPILOG   = 'ISSI - Inventario de sistemas de información'

CATALOG  = 'https://datos.canarias.es/catalogos/general/'
DATASET  = 'dataset/019f9d7e-64bc-4603-a306-45ca1902b13e'
RESOURCE = 'resource/59abb23f-1087-4996-8697-a447b28aaf87'
FILENAME = 'organigrama.csv'

SEP = '/'

RED       = colorama.Fore.RED
YELLOW    = colorama.Fore.YELLOW
BRIGHT    = colorama.Style.BRIGHT
GREEN     = colorama.Fore.GREEN
RESET_ALL = colorama.Style.RESET_ALL

VALID_DAYS = 15



def descargar_organigrama():
    target_file = settings.BASE_DIR / Path(FILENAME)
    if target_file.exists():
        stat = target_file.stat()
        mod_date = DateTime.fromtimestamp(stat.st_mtime)
        delta = DateTime.now() - mod_date
        if delta.days <= VALID_DAYS:  # Local file is still valid
            return target_file
    self.warning(f'El fichero local {target_file} no existe o está desfasado')
    url = f'{CATALOG}/{DATASET}/{RESOURCE}/download/{FILENAME}'
    urlretrieve(url, target_file)
    self.success('Fichero {target_file} descargado')
    return target_file


class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        colorama.just_fix_windows_console()
        super().__init__(*args, **kwargs)

    def warning(self, msg: str):
        self.stdout.write(
            f'{YELLOW}Atención{RESET_ALL} {BRIGHT}{msg}{RESET_ALL}'
            )
        
    def success(self, msg: str):
        self.stdout.write(
            f'{GREEN}OK{RESET_ALL}: {BRIGHT}{msg}{RESET_ALL}'
            )

    def panic(self, msg: str):
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
    
    def handle(self, *args, **options):
        id_dir3 = options.get('dir3')
        id_dircac = options.get('id')
        if id_dir3:
            print(f'Generar informe para DIR3 {id_dir3}')
            self.warning('Aun por implementar')
        elif id_dircac:
            print(f'Generar informe para DIRCAC {id_dircac}')
            self.warning('Aun por implementar')
        with open(descargar_organigrama(), 'r', encoding='utf-8') as source:
            reader = csv.reader(source, delimiter=';', quotechar='"')
            next(reader) # Ignorar primera fila de nombres
            mapa = dict()
            for row in reader:
                id_organismo = clean_integer(row[0])
                dir3 = clean_text(row[1])
                nombre_organismo = clean_text(row[3])
                id_sirhus = clean_integer(row[2])
                categoria = clean_text(row[4])
                depende_de_id = clean_integer(row[7])
                if depende_de_id == 1:
                    depende_de_id = None
                mapa[id_organismo] = {
                    'nombre_organismo': nombre_organismo,
                    'dir3': dir3,
                    'id_sirhus': id_sirhus,
                    'categoria': categoria,
                    'depende_de_id': depende_de_id,
                    }
            for id_organismo in mapa:
                row = mapa[id_organismo]
                steps = []
                id_parent = row.get('depende_de_id', None)
                while id_parent:
                    steps.insert(0, str(id_parent))
                    id_parent = mapa.get(id_parent, {}).get('depende_de_id', None)
                row['ruta'] = ruta = SEP + SEP.join(steps)
                try:
                    with transaction.atomic():
                        organismo, created = models.Organismo.upsert(
                            id_organismo,
                            **row,
                            )
                    if created:
                        self.success(f'Organismo {organismo} creado')
                    else:
                        self.success(f'Organismo {organismo} actualizado')
                except IntegrityError as err:
                    self.panic(
                        f'{err}: saving/updating {id_organigrama}'
                        )
                    self.warning(
                        f'{err}: saving/updating {id_organigrama}'
                        )
