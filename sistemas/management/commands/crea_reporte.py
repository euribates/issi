#!/usr/bin/env python3

import dataclasses
import argparse

import csv
from fpdf import FPDF
import colorama
from django.core.management.base import BaseCommand
from fpdf import FPDF

from comun.opendata import procedimientos
from comun.opendata import servicios
from directorio import models


CMD_NAME = 'crea_reporte'
ABOUT    = 'Crea un informe indivizualizado por organismo'
EPILOG   = 'ISSI - Inventario de sistemas de información'

WHITE  = colorama.Fore.WHITE
YELLOW = colorama.Fore.YELLOW
RED    = colorama.Fore.RED
BRIGHT = colorama.Style.BRIGHT
GREEN  = colorama.Fore.GREEN
RESET  = colorama.Style.RESET_ALL


class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        colorama.just_fix_windows_console()
        super().__init__(*args, **kwargs)

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def warning(self, msg: str):
        print(
            f'{YELLOW}Atención{RESET} {BRIGHT}{msg}{RESET}',
            file=self.stdout.write,
            )
        
    def success(self, msg: str):
        print(
            f'{GREEN}OK{RESET}: {BRIGHT}{msg}{RESET}',
            file=self.stdout.write,
            )

    def panic(self, msg: str):
        print(
            f'{RED}Error{RESET}: {BRIGHT}{msg}{RESET}',
            file=self.stderr
            )

    def error_falta_ente(self, tag=''):
        if tag:
            self.panic(f'El identificador del ente «{tag}» es incorrecto')
        else:
            self.panic('No se ha especificado el ente')
        print(f'\n{GREEN}Los valores aceptados son:{RESET}', file=self.stderr)
        for ente in models.Ente.objects.all():
            print(
                f'  {BRIGHT}{WHITE}{ente.pk}{RESET} {WHITE}{ente.organismo.nombre_organismo}{RESET}',
                file=self.stderr
                )
        return None

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['add_help'] = False
        result = super().create_parser(prog_name, subcommand, **kwargs)
        return result

    def add_arguments(self, parser):
        parser.add_argument('tag', help='Especificar el ente', nargs='?', default=None)
        parser.add_argument(
            '-h', '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Muestra la ayuda',
            )

    
    def add_jerarquia(self, pdf, organismo) -> set:
        pdf.set_font('helvetica', size=12)
        result = set()
        for org, level in organismo.iter_jerarquia():
            indent = '    ' * level
            pdf.cell(text=f'{indent}{org}')
            pdf.cell(text=f' [{org.dir3}]')
            pdf.ln(10)
            result.add(org.dir3)
        return result

    def add_catalogo_datos_abiertos(self, pdf, ente):
        pdf.add_page()
        pdf.set_font('helvetica', size=18)
        pdf.cell(text='Datos abiertos publicados en el catálogo')
        pdf.ln(10)
        pdf.set_font('helvetica', size=12)
        for (url, desc) in ente.get_open_data():
            pdf.cell(w=0, text=desc, link=url)
            pdf.ln(10)


    def handle(self, *args, **options):
        tag = options.get('tag')
        if not tag:
            return self.error_falta_ente()
        ente = models.Ente.load_ente(tag)
        if not ente:
            return self.error_falta_ente(tag)


        organismo = ente.organismo
        self.stdout.write(f'Generar informe para {organismo} [{organismo.dir3}]')
        filename = f'{tag}.pdf'
        self.stdout.write(filename, ending=' ')
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', size=24)
        pdf.cell(text=organismo.nombre_organismo)
        pdf.ln(14)
        pdf.set_font('helvetica', size=18)
        pdf.cell(text='Organigrama')
        pdf.ln(10)
        all_dir3 = self.add_jerarquia(pdf, organismo)
        pdf.add_page()
        pdf.set_font('helvetica', size=18)
        pdf.cell(text='Procedimientos')
        pdf.ln(10)
        pdf.set_font('helvetica', size=12)
        with open(procedimientos.descargar_datos(), 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Ignorar cabecera
            for line in reader:
                dir3 = line[7]
                if dir3 in all_dir3:
                    codigo = line[0]
                    name = line[1]
                    pdf.cell(text=codigo)
                    pdf.write(text=name)
                    pdf.ln(11)

        pdf.add_page()
        pdf.set_font('helvetica', size=18)
        pdf.cell(text='Carta de servicios')
        pdf.ln(10)
        pdf.set_font('helvetica', size=12)
        with open(servicios.descargar_datos(), 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Ignorar cabecera
            for line in reader:
                dir3 = line[7]
                if dir3 in all_dir3:
                    codigo = line[0]
                    name = line[1]
                    pdf.cell(text=codigo)
                    pdf.write(text=name)
                    pdf.ln(11)
        if organismo.ente:
            self.add_catalogo_datos_abiertos(pdf, ente)

        pdf.output(filename)
        self.stdout.write(f'{GREEN}✓{RESET}')
