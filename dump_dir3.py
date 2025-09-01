#!/usr/bin/env python3

import sys
import dataclasses
import csv

from filters import clean_text
from filters import clean_integer
from filters import slugify


@dataclasses.dataclass
class Organismo:
    """Estructura de datos para DIR3.
    """
    id_dir3: str
    id_sirhus: int
    nombre_organismo: str
    nivel: int
    tipo: str
    depende_de: str
    es_superior: bool
    childs: set = dataclasses.field(default_factory=set)

    def __eq__(self, other):
        return self.id_dir3 == other.id_dir3

    def __lt__(self, other):
        return self.nombre_organismo < other.nombre_organismo

    def __le__(self, other):
        return self.nombre_organismo <= other.nombre_organismo

    def __gt__(self, other):
        return self.nombre_organismo > other.nombre_organismo

    def __ge__(self, other):
        return self.nombre_organismo >= other.nombre_organismo

    def __str__(self):
        return (
            f'{self.es_superior} {self.id_dir3} {self.nombre_organismo}'
            f' {self.nivel} {self.tipo} <-- {self.depende_de} [{len(self.childs)}]'
            )

    def __hash__(self):
        return hash(self.id_dir3)

    def add(self, item):
        self.childs.add(item)
    
    def get_filename(self, ext='csv'):
        return f'{slugify(self.nombre_organismo)}-{self.id_dir3}.{ext}'


def iter_organigrama():
    """Iterador sobre el organigrama.
    """
    with open('organigrama.csv', 'r', encoding='utf-8') as source:
        reader = csv.reader(source, delimiter=';', quotechar='"')
        next(reader) # Ignorar primera fila de nombres
        for row in reader:
            yield Organismo(
                id_dir3=row[1],
                id_sirhus=clean_integer(row[2]),
                nombre_organismo=clean_text(row[3]),
                nivel=clean_integer(row[4]),
                tipo=row[5],
                depende_de=row[7],
                es_superior=(row[7] == 'A05003638'),
                )


def create_map() -> dict:
    """Devuelve el mapa del organigrama.
    """
    orgs = list(iter_organigrama())
    orgs_map = { org.id_dir3: org for org in orgs }
    for org in orgs:
        if org.depende_de in orgs_map:
            orgs_map[org.depende_de].add(org)
    return orgs_map


def create_tree(orgs_map) -> set:
    return {org for org in orgs_map.values() if org.es_superior }


def list_organismo(id_dir3, level=0, tree=None):
    """Lista los organismos dependedientes de otro.
    """
    if tree is None:
        tree = create_map()
    org = tree[id_dir3]
    print(
        '   ' * level,
        '└' if level > 0 else ' ',
        org.nombre_organismo,
        org.id_dir3,
        )
    for child in sorted(org.childs):
        list_organismo(child.id_dir3, level+1, tree=tree)


def iter_organismo(org):
    for child in org.childs:
        yield from iter_organismo(child)
    yield org


def list_top():
    """Lista todos los organismos de nivel superior.
    """
    tree = create_tree(create_map())
    for org in tree:
        filename = org.get_filename()
        print(f'Creando {filename}', end=' ')
        orgs = sorted(iter_organismo(org))
        with open(filename, 'w', encoding="utf-8") as f_out:
            print('nombre_organismo;DIR3', file=f_out)
            for _ in orgs:
                print('.', end='')
                print(f'"{_.nombre_organismo}";"{_.id_dir3}"', file=f_out)
        print('[OK]')




def travel(org):
    yield org
    if org.childs:
        for child in org.childs:
            yield from travel(child)


def make_graph(id_dir3=None):
    if id_dir3 is None:
        with open('organigrama.dot', 'w') as f_out:
            f_out.write('digraph organigrama {\n')
            f_out.write('    rankdir=LR\n')
            for org in iter_organigrama():
                f_out.write(
                    f'    {org.id_dir3}'
                    f' [label="{org.nombre_organismo}"]\n'
                    )
                f_out.write(f'    {org.depende_de} -> {org.id_dir3}')
            f_out.write('}')
    else:
        orgs = create_map()
        org = orgs[id_dir3]
        filename = org.get_filename('dot')
        print(f'Creado {filename}', end=' ')
        with open(filename, 'w', encoding='utf-8') as f_out:
            f_out.write('digraph {\n')
            f_out.write('    rankdir=LR\n')
            for node in travel(org):
                print('.', end='')
                f_out.write(
                    f'    {node.id_dir3}'
                    f' [label="{node.nombre_organismo}"]\n'
                    )
                f_out.write(f'    {node.depende_de} -> {node.id_dir3}\n')
            f_out.write('}')
        print('[Ok]')







if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        list_top()
        make_graph()
    if argc == 2:
        id_dir3 = sys.argv[1]
        print(f'Analizando {id_dir3}')
        list_organismo(id_dir3)
        make_graph(id_dir3)
