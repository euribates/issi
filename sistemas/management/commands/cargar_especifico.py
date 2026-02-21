#!/usr/bin/env python3

import random
from pathlib import Path

from django.core.management.base import BaseCommand

# import pandas as pd
from rich.console import Console
from rich.progress import track

from sistemas import models


CMD_NAME = 'cargar_especifico'
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

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            help='Especificar el archivo ODS',
            )
        parser.add_argument('-c', '--codigo', nargs='+')

    def warning(self, msg: str):
        self.console.print(f'[bold][yellow]Atención:[/yellow] {msg}[/bold]')
        
    def success(self, msg: str):
        self.console.print(f'[bold][green]OK:[/green] {msg}[/bold]')

    def panic(self, msg: str):
        self.console.print(f'[bold][red]Error:[/red] {msg}[/bold]')

    def handle(self, *args, **options):
        """Punto de entrada.
        """
        filename = Path(options.get('filename'))
        self.console.print(f"Procesando fichero libreOffice [bold]{filename}[bold]")
        codigos = options.get('codigo')
        for codigo in codigos:
            sistema = models.Sistema.load_sistema_por_codigo(codigo)
            for pregunta in track(models.Pregunta.objects.all()):
                opciones = list(pregunta.opciones.all())
                if opciones:
                    opcion = random.choice(opciones)
                    opcion.asignar_respuesta(sistema)

        # df = pd.read_excel(filename, engine="odf")
        # assert isinstance(df, pd.DataFrame)
        # self.out(f'Hay [bold]{len(df)}[/] registros')
        # df = self.rename_headers(df)
        # df = df.drop(columns=['estado', 'departamento'])
        # existentes = num_total = num_correctos = num_erroneos = 0
        # sigo = 'n'
        # for index, row in df.iterrows():
            # num_total += 1
            # num_linea = index + 1
            # row = tuple(row)
            # data = parse_row(row, n_linea=num_linea)

            # if data['uuid'].is_success() and data['uuid'].value:
                # uuid = data['uuid'].value
            # else:
                # uuid = None

            # num_errores = count_all_errors(data)
            # self.out(f'[[bold]{num_linea:6d}[/]', end='] ')
            # if has_minimum(data):
                # num_correctos += 1
                # codigo = data['codigo'].value
                # nombre_sistema = data['nombre_sistema'].value
                # self.out(
                    # f'[white]{codigo}[/] {nombre_sistema} {num_errores} errores',
                    # end=' ',
                    # )
            # else:
                # num_erroneos += 1
                # self.out(f'[red]{num_errores}[/] errores. Inválido', end=' ')
            # if uuid:
                # sistema = Sistema.load_sistema_por_uuid(uuid)
                # if sistema:
                    # self.out(f'[yellow]UUID {uuid}[/] [green]correcto[/]')
                    # existentes += 1
            # else:
                # self.out('[red]No UUID[/]')
            # self.out()
            # if num_errores:
                # for name, result in data.items():
                    # if result.is_failure():
                        # self.out('\n'.join(wrap(
                            # f"{name}: {result.error_message}",
                            # width=65,
                            # initial_indent='\t- ',
                            # subsequent_indent='\t',
                            # )))
            # self.out()
            # if sigo != 'a':
                # sigo = input('Sigo? [S]|n|a :').lower()
                # if sigo == 'n':
                    # break
        # self.out(f'Total de registros: [bold]{num_total:>9}[/]')
        # self.out(f'    Pre existentes: [bold]{existentes:>9}[/]')
        # self.out(f'       con errores: [bold]{num_erroneos:>9}[/]')
        # self.out(f'       insertables: [bold]{num_correctos:>9}[/]')

