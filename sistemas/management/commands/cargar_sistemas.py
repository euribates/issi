#!/usr/bin/env python3

from pathlib import Path

from django.core.management.base import BaseCommand

import pandas as pd
from rich.console import Console

from sistemas.parsers import parse_row


CMD_NAME = 'cargar_sistemas'
ABOUT    = 'Cargar los sistemas a partir de la hoja de cálculo'
EPILOG   = 'ISSI - Inventario de sistemas de información'


def clean_text(text: str) -> str|None:
    """Limpia el texto de entrada.
    """
    if text == '':
        return None
    text = text.strip()
    if text[0] == text[-1] == '"':
        text = text[1:-1]
    return text or None


class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(file=self.stdout)

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def shout(self, msg: str):
        self.console.print(msg, end=' ')

    def out(self, msg: str):
        self.console.print(msg, end='\n')

    def warning(self, msg: str):
        self.console.print(f'[bold][yellow]Atención:[/yellow] {msg}[/bold]')
        
    def success(self, msg: str):
        self.console.print(f'[bold][green]OK:[/green] {msg}[/bold]')

    def panic(self, msg: str):
        self.console.print(f'[bold][red]Error:[/red] {msg}[/bold]')

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            help='Especificar el archivo ODS',
            )

    def rename_headers(self, df):
        origin_names = list(df.columns)
        return df.rename(columns={
            origin_names[0]: 'estado',
            origin_names[1]: 'departamento',
            origin_names[2]: 'nombre_sistema',
            origin_names[3]: 'codigo',
            origin_names[4]: 'finalidad',
            origin_names[5]: 'materia',
            origin_names[6]: 'dir3',
            origin_names[7]: 'responsables_tecnologicos',
            origin_names[8]: 'responsables_funcionales',
            origin_names[9]: 'juriscan',
            origin_names[10]: 'comentarios',
            origin_names[11]: 'uuid',
            })

    def handle(self, *args, **options):
        """Punto de entrada.
        """
        filename = Path(options.get('filename'))
        self.shout(f"Procesando fichero libreOffice [bold]{filename}[bold]")
        df = pd.read_excel(filename, engine="odf")
        assert isinstance(df, pd.DataFrame)
        print(f'Hay {len(df)} registros')
        df = self.rename_headers(df)
        df = df.drop(columns=['estado', 'departamento'])
        for index, row in df.iterrows():
            row = tuple(row)
            data = parse_row(row, n_linea=index+1)
            for name in data:
                print(f'{name}: {type(data[name])!r}')
            print(index, data['nombre_sistema'], everything_pass(data))


def everything_pass(data):
    return all([
        isinstance(v, set) or v.is_success() for name, v in data.items()
        ])
