#!/usr/bin/env python3

import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

import pandas as pd
from rich.console import Console

from sistemas.models import Usuario, Interlocutor
from sistemas.models import Sistema
from directorio.models import Organismo


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
            help='Especificar el archivo CSV o ODS',
            )

    def rename_headers(df):
        origin_names = list(df.keys())
        df.rename(columns={
            origin_names[0]: 'estado',
            origin_names[1]: 'departamento',
            origin_names[2]: 'nombre_sistema',
            origin_names[3]: 'codigo',
            origin_names[4]: 'proposito',
            origin_names[5]: 'materia',
            origin_names[6]: 'dir3',
            origin_names[7]: 'responsables_tecnologicos',
            origin_names[8]: 'responsables_funcionales',
            origin_names[9]: 'juriscan',
            origin_names[10]: 'comentarios',
            origin_names[11]: 'estado',
            origin_names[12]: 'estado',


            }
    def handle(self, *args, **options):
        """Punto de entrada.
        """
        filename = Path(options.get('filename'))
        ext = filename.suffix.lower()
        match ext:
            case '.csv':
                self.shout(f"Procesando fichero CCS [bold]{filename}[bold]")
                df = pd.read_csv(filename)
            case '.ods':
                self.shout(f"Procesando fichero libreOffice [bold]{filename}[bold]")
                df = pd.read_excel(filename, engine="odf")
            case _:
                raise CommandError(f"No sé como procesar el fichero {filename}")
        print(f'Hay {len(df)} registros')
        print('Columnas:')
        for name in df.keys():
            print(name)
        return
        with open(filename, 'r', encoding='utf-8') as f_in:
            reader = csv.reader(f_in)
            next(reader)  # Ignoramos la línea de cabecera
            for row in reader:
                dir3 = clean_text(row[3])
                organismo = Organismo.load_organismo_using_dir3(dir3)
                nombre = clean_text(row[7])
                apellidos = clean_text(row[8])
                email = clean_text(row[10])
                username = email.rsplit('@', 1)[0]
                usuario = Usuario.load_usuario(username)
                if usuario:
                    self.console.print(
                        f"Usuario [bold]{username}[/]"
                        f" ({nombre} {apellidos})"
                        " [yellow]Ya existe[/], lo ignoramos"
                        )
                else:
                    self.console.print(
                        f"Usuario [bold]{username}[/]"
                        f" ({nombre} {apellidos})"
                        " no existe, lo crearemos"
                        )
                    usuario = Usuario(
                        login=username,
                        email=email,
                        nombre=nombre,
                        organismo=organismo,
                        apellidos=apellidos,
                        )
                    usuario.save()
                if organismo:
                    _interlocutor, created = Interlocutor.upsert(
                        usuario=usuario,
                        organismo=organismo,
                        )
                    if created:
                        self.console.print("[green]Creado[/] como interlocutor")
        return
