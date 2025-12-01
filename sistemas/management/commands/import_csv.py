#!/usr/bin/env python3

import sys
import uuid
import argparse
import csv
from pathlib import Path
from html import escape

from django.conf import settings
from django.core.management.base import BaseCommand
from rich.console import Console
from rich.table import Table

from comun.filters import slugify
from directorio.models import Ente
from directorio.models import Organismo
from sistemas.models import Tema
from sistemas.models import Sistema
from sistemas.models import Perfil
from sistemas.models import NormaSistema
from sistemas import parsers
from comun.funcop import static


INPUT_DIR = settings.BASE_DIR / 'imports'

CMD_NAME = 'import_csv'
ABOUT    = 'Importa la hoja de datos de un ente'
EPILOG   = 'ISSI - Inventario de sistemas de información'


@static(codigos=set([]))
def codigo_no_repetido(linea, codigo):
    if codigo in codigo_no_repetido.codigos:
        return (
            f'En la línea {linea} aparece un codigo interno {escape(codigo)}'
            ' que ya había sido utilizado'
            )
    codigo_no_repetido.codigos.add(codigo)
    return None


def msg_falta_tema(materia):
    return (
        'No entiendo la materia referencial'
        f' indicada: {escape(materia)}.'
        )


def add_sistema(payload):
    jursican = payload.pop('juriscan', [])
    responsables_tecnologicos = payload.pop('responsables_tecnologicos', [])
    responsables_funcionales = payload.pop('responsables_funcionales', [])
    sistema = Sistema(**payload)
    sistema.save()
    for codigo_juriscan in juriscan:
        NormaSistema.upsert(sistema, codigo_juriscan)
    for usr in responsables_tecnologicos:
        Perfil.upsert(sistema, usr.login, 'TEC')
    for usr in responsables_funcionales:
        Perfil.upsert(sistema, usr.login, 'FUN')
    return sistema


def update_sistema(payload):
    jursican = payload.pop('juriscan', [])
    responsables_tecnologicos = payload.pop('responsables_tecnologicos', [])
    responsables_funcionales = payload.pop('responsables_funcionales', [])
    sistema = Sistema.load_sistema_por_uuid(payload['uuid'])
    num_cambios = 0
    if sistema.nombre_sistema != payload['nombre_sistema']:
        sistema.nombre_sistema = payload['nombre_sistema']
        num_cambios += 1
    if sistema.organismo != payload['organismo']:
        sistema.organismo = payload['organismo']
        num_cambios += 1
    if sistema.proposito != payload['proposito']:
        sistema.proposito = payload['proposito']
        num_cambios += 1
    if sistema.descripcion != payload['descripcion']:
        sistema.descripcion = payload['descripcion']
        num_cambios += 1
    if sistema.observaciones != payload['observaciones']:
        sistema.observaciones = payload['observaciones']
        num_cambios += 1
    if sistema.tema != payload['tema']:
        sistema.tema = payload['tema']
        num_cambios += 1
    if num_cambios > 0:
        sistema.save()
    needs_touch = False
    for codigo_juriscan in juriscan:
        _, created = NormaSistema.upsert(sistema, codigo_juriscan)
        needs_touch = needs_touch or _created
    for usr in responsables_tecnologicos:
        _, created = Perfil.upsert(sistema, usr.login, 'TEC')
        needs_touch = needs_touch or _created
    for usr in responsables_funcionales:
        _, created = Perfil.upsert(sistema, usr.login, 'FUN')
        needs_touch = needs_touch or _created
    if needs_touch:
        sistema.touch()
    return sistema


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
        for ente in Ente.objects.all():
            table.add_row(ente.pk, ente.organismo.nombre_organismo)
        self.console.print(table)
        return None


    def handle(self, *args, **options):
        tag = options.get('tag')
        if not tag:
            return self.error_falta_ente()
        ente = Ente.load_ente(tag)
        if not ente:
            return self.error_falta_ente(tag)

        input_filename = INPUT_DIR / Path(f"{tag}.csv")
        errors = []
        warnings = []
        inserts = []
        updates = []
        with open(input_filename, 'r', encoding="utf-8") as input_file:
            reader = csv.reader(input_file, delimiter=',', quotechar='"')
            first_line = next(reader) # Ignoramos la primera línea
            num_cols = len(first_line) # excepto para saber cuantas columnas hay
            print(f'Detectadas {num_cols} columnas')
            assert 9 <= num_cols < 11, f"El Número de columnas debe ser 9 o 10, no {num_cols}"
            for linea, tupla in enumerate(reader, start=1):
                assert len(tupla) == num_cols 
                nombre_sistema = tupla[0]
                cii = slugify(tupla[1]).strip().upper()
                if not cii:
                    errors.append(f'En línea {linea}, no se ha definido un código interno')
                error = codigo_no_repetido(linea, cii)
                if error:
                    errors.append(error)
                finalidad = tupla[2]
                materia_competencial = tupla[3].strip()
                if not materia_competencial:
                    warnings.append(f'En la fila {linea}, el S.I. No tiene tema asignado')
                else:
                    tema = Tema.load_tema(materia_competencial)
                    if not tema:
                        tema = Tema.load_tema_por_nombre(materia_competencial)
                    if not tema:
                        errors.append(
                            f'En la fila {linea}:'
                            f' El tema {materia_competencial}'
                            ' no existe'
                            )
                        tema = Tema.load_tema('UNK')
                dir3 = tupla[4]
                organismo = Organismo.load_organismo_using_dir3(dir3)
                responsables_tecnologicos =  parsers.parse_users(tupla[5])
                responsables_funcionales =  parsers.parse_users(tupla[6])
                juriscan = parsers.parse_juriscan(tupla[7])
                comentarios = tupla[8]
                verbose = not False
                if verbose:
                    print(f'Nombre del sistema: {nombre_sistema}')
                    print(f'Código interno: {cii}')
                    print(f'Finalidad: {finalidad}')
                    print(f'Materia conpetencial:: {materia_competencial}')
                    print(f'DIR3: {dir3}')
                    print(f'Organismo: {organismo}')
                    print(f'Responsables tecnologicos: {responsables_tecnologicos}')
                    print(f'Responsables funcionales: {responsables_funcionales}')
                    print(f'Juriscan: {juriscan!r}')
                    print(f'Comentarios: {comentarios!r}')

                if num_cols == 10:
                    uuid_sistema = tupla[9]
                    if verbose:
                        print(f'UUID: {uuid_sistema!r}')
                    if not Sistema.load_sistema_por_uuid(uuid_sistema):
                        errors.append(
                            f'No existe ningún sistema con UUID {escape(uuid_sistema)}'
                            )
                else:
                    uuid_sistema = None

                sublines = finalidad.splitlines()
                if len(sublines) == 1:
                    proposito = sublines[0]
                    descripcion = ''
                else:
                    proposito = sublines[0]
                    descripcion = '\n\n'.join(sublines[1:])

                payload = {
                    'uuid': uuid_sistema,
                    'nombre_sistema': nombre_sistema,
                    'organismo': organismo,
                    'codigo': cii,
                    'proposito': proposito,
                    'descripcion': descripcion,
                    'observaciones': comentarios,
                    'tema': tema,
                    'juriscan': juriscan,
                    'responsables_tecnologicos': responsables_tecnologicos,
                    'responsables_funcionales': responsables_funcionales,
                    }
                if uuid:
                    updates.append(payload)
                else:
                    inserts.append(payload)
                if verbose:
                    print()
                else:
                    print('█', end='')
                # if linea > 3:
                    # break
            print()
        if errors or warnings:
            sys.stdout.flush()
            sys.stderr.flush()
            for msg in warnings:
                sys.stderr.write(f'Warning: {msg}\n')
            for err in errors:
                sys.stderr.write(f'Error: {err}\n')
        else:
            print('Todo OK')
            print(f'A punto de añadir {len(inserts)} sistemas nuevos')
            for payload in inserts:
                sistema = add_sistema(payload)
                print(f'- Creado {sistema} [OK]')
            print(f'A punto de actualizar {len(updates)} sistemas ya existentes')
            for payload in inserts:
                sistema = update_sistema(payload)
                print(f'- Actualizado {sistema} [OK]')

