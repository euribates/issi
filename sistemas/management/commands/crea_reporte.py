#!/usr/bin/env python3

import argparse
import collections
import csv
import dataclasses

from django.conf import settings
from django.core.management.base import BaseCommand
from fpdf import FPDF
from fpdf.fonts import FontFace
from rich.console import Console
from rich.table import Table

from comun.funcop import agrupa
from comun.opendata import procedimientos
from comun.opendata import servicios
from directorio.models import Ente


OUTPUT_DIR = settings.BASE_DIR / 'reportes'

CMD_NAME = 'crea_reporte'
ABOUT    = 'Crea un informe indivizualizado por organismo'
EPILOG   = 'ISSI - Inventario de sistemas de información'


class REPORTE_GOBCAN(FPDF):

    def footer(self):
        self.set_y(-15)  # Position cursor at 1.5 cm from bottom:
        self.set_font("dejavu-sans", style="I", size=8)
        text = f"Gobierno de Canarias - {self.filename} - Page {self.page_no()}/{{nb}}"
        self.cell(0, 10, text=text, align="C")

    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = filename
        self.add_font("dejavu-sans", style="", fname="./fonts/DejaVuSans.ttf")
        self.add_font("dejavu-sans", style="b", fname="./fonts/DejaVuSans-Bold.ttf")
        self.add_font("dejavu-sans", style="i", fname="./fonts/DejaVuSans-Oblique.ttf")
        self.add_font("dejavu-sans", style="bi", fname="./fonts/DejaVuSans-BoldOblique.ttf")
        self.set_font('dejavu-sans', size=12)

    def seccion(self, titulo, new_page=True):
        if new_page:
            self.add_page()
        self.set_font('dejavu-sans', size=18)
        self.set_text_color(r=33, g=33, b=128)
        self.cell(text=titulo, align='C')
        self.ln(20)
        self.set_font('dejavu-sans', size=12)
        self.set_text_color(r=0, g=0, b=0)

    def h2(self, titulo):
        self.set_font('dejavu-sans', size=14, style='B')
        self.cell(w=0, text=titulo)
        self.ln(20)
        self.set_font('dejavu-sans', size=12)

    def as_url(self, url):
        self.set_font('courier', size=10)
        self.set_text_color(r=33, g=33, b=128)
        self.set_x(15)
        self.cell(text=url, link=url)
        self.set_font('dejavu-sans', size=12)
        self.set_text_color(r=0, g=0, b=0)
        self.ln(11)




class Command(BaseCommand):
    help = ABOUT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(file=self.stdout)

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def warning(self, msg: str):
        self.console.print(f'[bold][yellow]Atención:[/yellow] {msg}[/bold]')
        
    def success(self, msg: str):
        self.console.print(f'[bold][green]OK:[/green] {msg}[/bold]')

    def panic(self, msg: str):
        self.console.print(f'[bold][red]Error:[/red] {msg}[/bold]')

    def error_falta_ente(self, tag=''):
        if tag:
            self.panic(f'El identificador del ente «{tag}» es incorrecto')
        else:
            self.panic('No se ha especificado el ente')
        self.console.print(f'Los valores aceptados son:')
        table = Table(title="Entes")
        table.add_column("Código", justify="right", style="bold")
        table.add_column("Nombre")
        for ente in Ente.objects.all():
            table.add_row(ente.pk, ente.organismo.nombre_organismo)
        self.console.print(table)
        return None

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['add_help'] = False
        result = super().create_parser(prog_name, subcommand, **kwargs)
        return result

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
    
    def add_jerarquia(self, pdf, organismo) -> dict:
        pdf.seccion('Organigrama y códigos DIR3', new_page=False)
        result = dict()
        white = (255, 255, 255)
        grey = (64, 64, 64)
        table_properties = {
            'col_widths': (80, 20),
            'text_align': ("LEFT", "RIGHT"),
            'padding': 2,
            'v_align': 'TOP',
            'borders_layout': 'INTERNAL',
            'headings_style': FontFace(color=white, fill_color=grey),
            }
        with pdf.table(**table_properties) as table:
            header = table.row()
            header.cell('Nombre')
            header.cell('Cod. DIR3')
            for org, level in organismo.iter_jerarquia():
                row = table.row()
                if level == 0:
                    pdf.set_font('dejavu-sans', size=13, style='B')
                elif level == 1:
                    pdf.set_font('dejavu-sans', size=12, style='B')
                else:
                    pdf.set_font('dejavu-sans', size=12, style='')
                row.cell(f'{org}', padding=(2, 2, 2, 2 + 3 * level))
                pdf.set_font('courier', size=12, style='B')
                row.cell(org.dir3)
                result[org.dir3] = org
        return result

    def add_procedimientos(self, all_dir3, pdf):
        pdf.seccion('Procedimientos')
        items = []
        Procedimiento = collections.namedtuple(
            'Procedimiento',
            ['dir3', 'nombre', 'codigo'],
            )
        with open(procedimientos.descargar_datos(), 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Ignorar cabecera
            for line in reader:
                dir3 = line[10]
                if dir3 in all_dir3:
                    codigo = line[0]
                    org = all_dir3[dir3]
                    nombre = line[1]
                    items.append(Procedimiento(dir3, nombre, codigo))
        items.sort()
        agrupado = agrupa(items)
        for dir3 in agrupado:
            rows = agrupado[dir3]
            pdf.set_font('dejavu-sans', size=14, style='B')
            nombre_organismo = all_dir3[dir3].nombre_organismo
            pdf.write(text=f'{nombre_organismo} ({len(rows)} procedimientos)')
            pdf.ln(11)
            for row in rows:
                pdf.set_font('dejavu-sans', size=12, style='')
                pdf.multi_cell(w=0, text=row.nombre, padding=(1, 1, 1, 4))
                pdf.ln(2)
                url = f'https://sede.gobiernodecanarias.org/sede/tramites/{row.codigo}'
                pdf.as_url(url)

    def add_servicios(self, all_dir3, pdf):
        pdf.seccion('Carta de servicios')
        white = (255, 255, 255)
        grey = (64, 64, 64)
        table_properties = {
            'col_widths': (80, 20),
            'text_align': ("LEFT", "RIGHT"),
            'padding': 2,
            'v_align': 'TOP',
            'borders_layout': 'INTERNAL',
            'headings_style': FontFace(color=white, fill_color=grey),
            }
        Servicio = collections.namedtuple('Servicio', ['dir3', 'nombre', 'codigo'])
        items = []
        with open(servicios.descargar_datos(), 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Ignorar cabecera
            for line in reader:
                dir3 = line[7]
                if dir3 in all_dir3:
                    items.append(Servicio(
                        dir3=dir3,
                        nombre=line[1],
                        codigo=int(line[0]),
                        ))
        items.sort()
        agrupado = agrupa(items)
        for dir3 in agrupado:
            nombre_organismo = all_dir3[dir3].nombre_organismo
            pdf.h2(nombre_organismo)
            with pdf.table(**table_properties) as table:
                row = table.row()
                row.cell('Nombre')
                row.cell('Cod. SiCAC')
                for _servicio in agrupado[dir3]:
                    row = table.row()
                    row.cell(text=_servicio.nombre)
                    row.cell(text=str(_servicio.codigo))

    def add_catalogo_datos_abiertos(self, pdf, ente: Ente):
        pdf.seccion('Datos abiertos publicados en el catálogo')
        for (url, desc) in ente.get_open_data():
            pdf.text(x=0, y=0, text=desc)
            pdf.ln(10)
            pdf.cell(w=0, text=url, link=url)
            pdf.ln(10)

    def handle(self, *args, **options):
        tag = options.get('tag')
        if not tag:
            return self.error_falta_ente()
        ente = Ente.load_ente(tag)
        if not ente:
            return self.error_falta_ente(tag)

        organismo = ente.organismo
        self.console.print(f'Generar informe para [bold]{organismo}[/bold] ({organismo.dir3})')

        if not OUTPUT_DIR.exists():
            OUTPUT_DIR.mkdir()
        filename = OUTPUT_DIR / f'{tag}.pdf'
        pdf = REPORTE_GOBCAN(filename)
        pdf.add_page()
        pdf.set_font('dejavu-sans', size=24)
        pdf.cell(text=organismo.nombre_organismo)
        pdf.ln(14)
        all_dir3 = self.add_jerarquia(pdf, organismo)
        self.add_procedimientos(all_dir3, pdf)
        self.add_servicios(all_dir3, pdf)
        self.add_catalogo_datos_abiertos(pdf, ente)
        pdf.output(filename)
        self.success(f'Archivo {filename} generado')
