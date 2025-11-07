#!/usr/bin/env python3

import csv

from django.core.management.base import BaseCommand

from rich.console import Console

from sistemas.models import Usuario, Interlocutor
from directorio.models import Organismo


CMD_NAME = 'cargar_interlocutores'
ABOUT    = 'Cargar los interlocutores por organismo'
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
            help='Especificar el archivo CSV',
            )

    def handle(self, *args, **options):
        """Punto de entrada.
        """
        filename = options.get('filename')
        if not filename:
            return "Error: no se ha especificado el fichero"
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
