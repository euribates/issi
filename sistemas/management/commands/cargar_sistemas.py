#!/usr/bin/env python3

from pathlib import Path

from django.core.management.base import BaseCommand

from rich.console import Console
from rich.table import Table

from sistemas.models import Sistema
from sistemas.importers import importar_sistemas_desde_fichero

CMD_NAME = 'cargar_sistemas'
ABOUT    = 'Cargar los sistemas a partir de la hoja de cálculo'
EPILOG   = 'ISSI - Inventario de sistemas de información'


class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(file=self.stdout)

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def out(self, msg: str = '', end='\n'):
        self.console.print(msg, end=end)

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            help='Especificar el archivo ODS',
            )

    def handle(self, *args, **options):
        """Punto de entrada.
        """
        filename = Path(options.get('filename'))
        self.out(f"Procesando fichero libreOffice [bold]{filename}[bold]")
        table = Table(title="Star Wars Movies")
        table.add_column("Código", justify="right", style="cyan", no_wrap=True)
        table.add_column("Nombre")
        table.add_column("Importable", justify="right")
        table.add_column("Errores", justify="right")
        table.add_column("UUID", justify="center")
        with open(filename, 'rb') as fp:
            existentes = num_total = num_correctos = num_erroneos = 0
            iter_sistemas = importar_sistemas_desde_fichero(fp.read())
            for index, data, pass_minimun, all_errors in iter_sistemas:
                num_total += 1
                if pass_minimun:
                    num_correctos += 1
                else:
                    num_erroneos += 1
                if data['codigo'].is_failure():
                    codigo = '[red]falta el código[/]'
                else:
                    codigo = data['codigo'].value
                if data['nombre_sistema'].is_failure():
                    nombre_sistema = '[red]falta el código[/]'
                else:
                    nombre_sistema = data['nombre_sistema'].value
                check_uuid = '[green]ok[/]'
                uuid = data['uuid'].value
                if uuid:
                    sistema = Sistema.load_sistema_por_uuid(uuid)
                    if sistema is None:
                        check_uuid = '[red]No existe[/]'
                    else:
                        existentes += 1
                table.add_row(
                    codigo,
                    nombre_sistema,
                    '[green]si[/]' if pass_minimun else '[red]no[/n]',
                    str(len(all_errors)),
                    check_uuid,
                    )
            self.out(table)
        self.out('Resumen:')
        self.out(f'Total de registros: [bold]{num_total:>9}[/]')
        self.out(f'    Pre existentes: [bold]{existentes:>9}[/]')
        self.out(f'       con errores: [bold]{num_erroneos:>9}[/]')
        self.out(f'       insertables: [bold]{num_correctos:>9}[/]')

            # if num_errores:
                # for name, result in data.items():
                    # if result.is_failure():
                        # self.out('\n'.join(wrap(
                            # f"{name}: {result.error_message}",
                            # width=65,
                            # initial_indent='\t- ',
                            # subsequent_indent='\t',
                            # )))




