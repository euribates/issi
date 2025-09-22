#!/usr/bin/env python3

import dataclasses

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

RED       = colorama.Fore.RED
BRIGHT    = colorama.Style.BRIGHT
GREEN     = colorama.Fore.GREEN
RESET_ALL = colorama.Style.RESET_ALL


class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        colorama.just_fix_windows_console()
        super().__init__(*args, **kwargs)

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

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

    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--tag',
            help='Especificar el ente',
            )
    
    def handle(self, *args, **options):
        tag = options.get('tag')
        if not tag:
            self.panic('No se ha especificado el ente')
            return None
        ente = models.Ente.load_ente(tag)
        if not ente:
            self.panic(
                f'El identificador del ente {tag}'
                ' no es correcto'
                )
            return None
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
        pdf.set_font('helvetica', size=12)
        all_dir3 = set()
        for org, level in organismo.iter_jerarquia():
            indent = '    ' * level
            pdf.cell(text=f'{indent}{org}')
            pdf.cell(text=f' [{org.dir3}]')
            pdf.ln(10)
            all_dir3.add(org.dir3)

        pdf.add_page()
        pdf.set_font('helvetica', size=18)
        pdf.cell(text='Procedimientos')
        pdf.ln(10)
        pdf.set_font('helvetica', size=12)
        with open(procedimientos.descargar_datos()) as f:
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
        with open(servicios.descargar_datos()) as f:
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

        pdf.output(filename)
        self.stdout.write(f'{GREEN}✓{RESET_ALL}')
