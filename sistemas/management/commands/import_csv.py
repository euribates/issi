#!/usr/bin/env python3

from uuid import uuid4
import argparse
import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from rich.console import Console
from rich.table import Table

from sistemas import models
from sistemas import parsers

INPUT_DIR = settings.BASE_DIR / 'imports'

CMD_NAME = 'import_csv'
ABOUT    = 'Importa la hoja de datos de un ente'
EPILOG   = 'ISSI - Inventario de sistemas de información'


class BaseOpCommand:

    def __init__(self, op_code: str, payload: dict):
        self.op_code = op_code
        self.payload = payload.copy()

    def __str__(self):
        return f'{self.op_code}: {self.payload!r}'


class UpdateSistema(BaseOpCommand):

    def __init__(self, payload):
        super().__init__('UPDATE', payload)
        id_sistema = self.payload['id_sistema']
        self.sistema = models.Sistema.load_sistema(id_sistema)
        self.juriscan = self.payload.pop('juriscan', [])
        self.responsables_tecnologicos = self.payload.pop('responsables_tecnologicos', [])
        self.responsables_funcionales = self.payload.pop('responsables_funcionales', [])

    def f_update(self, field_name):
        old_value = getattr(self.sistema, field_name)
        new_value = self.payload[field_name]
        if old_value != new_value:
            setattr(self.sistema, field_name, new_value)
            return 1
        return 0

    def __call__(self):
        n_cambios = 0
        n_cambios += self.f_update('nombre_sistema')
        n_cambios += self.f_update('organismo')
        n_cambios += self.f_update('finalidad')
        n_cambios += self.f_update('descripcion')
        n_cambios += self.f_update('observaciones')
        n_cambios += self.f_update('tema')
        if n_cambios > 0:
            self.sistema.save()
        needs_touch = False
        for codigo_juriscan in self.juriscan:
            _, created = models.NormaSistema.upsert(self.sistema, codigo_juriscan)
            needs_touch = needs_touch or created
        for usr in self.responsables_tecnologicos:
            usuario = models.Usuario.load_usuario(usr['login'])
            if not usuario:
                usuario = models.Usuario(**usr)
                usuario.save()
            _, created = models.Perfil.upsert(self.sistema, usuario, 'TEC')
            needs_touch = needs_touch or created
        for usr in self.responsables_funcionales:
            usuario = models.Usuario.load_usuario(usr['login'])
            if not usuario:
                usuario = models.Usuario(**usr)
                usuario.save()
            _, created = models.Perfil.upsert(self.sistema, usuario, 'FUN')
            needs_touch = needs_touch or created
        if needs_touch:
            self.sistema.touch()
        return self.sistema


class InsertSistema(BaseOpCommand):

    def __init__(self, payload):
        super().__init__('INSERT', payload)
        self.juriscan = self.payload.pop('juriscan', [])
        self.responsables_tecnologicos = self.payload.pop('responsables_tecnologicos', [])
        self.responsables_funcionales = self.payload.pop('responsables_funcionales', [])
        
    def __call__(self):
        if not self.payload['uuid_sistema']:
            self.payload['uuid_sistema'] = uuid4()
        sistema = models.Sistema(**self.payload)
        sistema.save()
        for codigo_juriscan in self.juriscan:
            models.NormaSistema.upsert(sistema, codigo_juriscan)
        for usr in self.responsables_tecnologicos:
            models.Perfil.upsert(sistema, usr.login, 'TEC')
        for usr in self.responsables_funcionales:
            models.Perfil.upsert(sistema, usr.login, 'FUN')
        return sistema


def chk_columnas(n_linea, row, min_cols=9, max_cols=10):
    n_cols = len(row)
    if n_cols < min_cols  or n_cols > max_cols:
        raise ValueError(
            f"En la linea {n_linea}, "
            "el número de columnas debe estar comprendido"
            f" entre {min_cols} y {max_cols}, ambas inclusive,"
            f" pero vale {n_cols}."
            )
    return n_cols


class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(file=self.stdout)

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        kwargs['add_help'] = False
        return super().create_parser(prog_name, subcommand, **kwargs)

    def warning(self, msg: str):
        self.console.print(f'[bold][yellow]Atención:[/yellow] {msg}[/bold]')
        
    def success(self, msg: str):
        self.console.print(f'[bold][green]OK:[/green] {msg}[/bold]')

    def panic(self, msg: str):
        self.console.print(f'[bold][red]Error:[/red] {msg}[/bold]')

    def add_arguments(self, parser):
        parser.add_argument(
            'tag',
            help='Especificar el ente',
            nargs='?',
            default=None,
            )
        parser.add_argument(
            '-h', '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Muestra la ayuda',
            )

    def error_falta_ente(self, tag=''):
        if tag:
            self.panic(f'El identificador del ente «{tag}» es incorrecto')
        else:
            self.panic('No se ha especificado el ente')
        self.console.print('Los valores aceptados son:')
        table = Table(title="Entes")
        table.add_column("Código", justify="right", style="bold")
        table.add_column("Nombre")
        for ente in models.Ente.objects.all():
            table.add_row(ente.pk, ente.organismo.nombre_organismo)
        self.console.print(table)
        return None

    def handle(self, *args, **options):
        tag = options.get('tag').upper()
        if not tag:
            return self.error_falta_ente()
        ente = models.Ente.load_ente(tag)
        if not ente:
            return self.error_falta_ente(tag)

        input_filename = INPUT_DIR / Path(f"{tag}.csv")
        commands = []
        errors = []
        with open(input_filename, 'r', encoding="utf-8") as input_file:
            reader = csv.reader(input_file, delimiter=',', quotechar='"')
            first_line = next(reader)      # Ignoramos la primera fila, excepto
            n_cols = chk_columnas(0, first_line)  # para saber cuantas columnas hay
            for n_linea, tupla in enumerate(reader, start=1):
                if len(tupla) != n_cols:
                    raise ValueError(
                        f'En la linea {n_linea},'
                        f' no coinciden el número de filas ({len(tupla)})'
                        f' con el esperado: {n_cols}.'
                        )
                row_errors, payload = parsers.parse_row(tupla, n_linea=n_linea)
                errors.extend(row_errors)
                # chk_codigo_no_repetido(payload['codigo'], n_linea=n_linea)

                print('█', end='')

                if payload['id_sistema']:
                    cmd = UpdateSistema(payload)
                    commands.append(cmd)
                else:
                    commands.append(InsertSistema(payload))
                # if n_linea > 3:
                    # break
            print()
        if not errors:
            print('Todo OK')
            print(f'A punto de realizar {len(commands)} operaciones en la BD')
            for _cmd in commands:
                print('call', end=' ')
                print(_cmd)
                _cmd()
                print('[OK]')
        else:
            print('Errores')
            for err in errors:
                print(str(err))
