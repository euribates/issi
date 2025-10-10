#!/usr/bin/env python3

from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
from pathlib import Path
import csv
from urllib.request import urlretrieve

from rich.console import Console
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from django.conf import settings
from filters import clean_text
from filters import clean_integer
from filters import clean_url
from directorio import models


CMD_NAME = 'importar_organigrama'
ABOUT    = 'Crea las tablas de organismos a partir del DIRCAC'
EPILOG   = 'ISSI - Inventario de sistemas de información'

CATALOG  = 'https://datos.canarias.es/catalogos/general/'
DATASET  = 'dataset/019f9d7e-64bc-4603-a306-45ca1902b13e'
RESOURCE = 'resource/59abb23f-1087-4996-8697-a447b28aaf87'
FILENAME = 'organigrama.csv'

SEP = '/'

VALID_DAYS = 15

TEMP_DIR = settings.BASE_DIR / Path('temp')
if not TEMP_DIR.is_dir():
    TEMP_DIR.mkdir()


class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        self.console = Console()
        super().__init__(*args, **kwargs)

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

    def warning(self, msg: str):
        self.console.print(f'[yellow]Atención[/] [bols]{msg}[/]')
        
    def success(self, msg: str):
        self.console.print(f'[green]OK[/]: [bold]{msg}[/]')

    def panic(self, msg: str):
        self.console.print(f'[red]Error[/]: [bold]{msg}[/]')

    def descargar_organigrama(self) -> Path:
        '''Descarga el organigrama desde el espacio de datos abiertos.

        Solo lo descarga si la copia local no existe o, aun
        existitendo, ha sido creada hace más de `VALID_DAYS`.

        Returns:

            La ruta del ficnero
        '''
        target_file = TEMP_DIR / FILENAME
        if target_file.exists():
            stat = target_file.stat()
            mod_date = DateTime.fromtimestamp(stat.st_mtime)
            delta = DateTime.now() - mod_date
            if delta.days <= VALID_DAYS:  # Local file is still valid
                return target_file
        self.warning(f'El fichero local [bold]{target_file}[/] no existe o está desfasado')
        url = f'{CATALOG}/{DATASET}/{RESOURCE}/download/{FILENAME}'
        urlretrieve(url, target_file)
        self.success('Fichero [bold]{target_file}[/] descargado')
        return target_file

    def handle(self, *args, **options):
        with open(self.descargar_organigrama(), 'r', encoding='utf-8') as source:
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
                url = clean_url(row[35])
                mapa[id_organismo] = {
                    'nombre_organismo': nombre_organismo,
                    'dir3': dir3,
                    'id_sirhus': id_sirhus,
                    'categoria': categoria,
                    'depende_de_id': depende_de_id,
                    'url': url,
                    }
            for id_organismo in mapa:
                row = mapa[id_organismo]
                nombre_organismo = row['nombre_organismo']
                steps = [str(id_organismo)]
                id_parent = row.get('depende_de_id', None)
                while id_parent:
                    steps.append(str(id_parent))
                    id_parent = mapa.get(id_parent, {}).get('depende_de_id', None)
                row['ruta'] = SEP + SEP.join(reversed(steps))
                try:
                    if models.Organismo.needs_update(id_organismo, row):
                        with transaction.atomic():
                            organismo, created = models.Organismo.upsert(id_organismo, **row)
                        if created:
                            self.success(f'Organismo {nombre_organismo} [red]creado[/]')
                        else:
                            self.success(f'Organismo {nombre_organismo} [yellow]actualizado[/]')
                    else:
                        self.success(f'Organismo {nombre_organismo} [green]sin cambios[/]')
                except IntegrityError as err:
                    self.panic(
                        f'{err}: saving/updating {id_organismo}'
                        )
                    self.warning(
                        f'{err}: saving/updating {id_organismo}'
                        )
