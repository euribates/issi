#!/usr/bin/env python3

import dataclasses

import colorama
from django.core.management.base import BaseCommand

from comun.opendata import 
CMD_NAME = 'crea_reporte'
ABOUT    = 'Crea un informe indivizualizado por organismo'
EPILOG   = 'ISSI - Inventario de sistemas de información'

RED = colorama.Fore.RED
RESET_ALL = colorama.Style.RESET_ALL

@dataclasses.dataclass
class OpenData:

    DATOS_CANARIAS = 'https://datos.canarias.es/catalogos/general'

    dataset: str
    resource: str
    filemame: str

    def url(self):
        '''Devuelve la URL de descarga del recurso.

        Ejemplo de uso:

            >>> servicios = OpenData(
            ...     dataset='41d56909-566f-4ab2-99e2-78a03577bb97',
            ...     resource='c636e6f7-e1a6-441a-9519-007ef69197e9',
            ...     filename='servicios.csv',
            ...     )
            >>> 
            >>> assert servicios.url() == (
            ...     'https://datos.canarias.es/catalogos/general/'
            ...     'dataset/41d56909-566f-4ab2-99e2-78a03577bb97/'
            ...     'resource/c636e6f7-e1a6-441a-9519-007ef69197e9/'
            ...     'download/servicios.csv'
            ...     )
        '''
        return '/'.join([
            DATOS_CANARIAS,
            'dataset',
            self.dataset,
            'resource',
            self.resource,
            'download',
            self.filename,
            ])
            


procedimientos = (
    dataset='946cdcde-2118-48ef-a30a-f9dc812c82db',
    resource='10b71b12-fb77-47b7-88f6-ec46ebee1548',
    filename='procedimientos.csv',
    )

servicios = OpenData(
    dataset='41d56909-566f-4ab2-99e2-78a03577bb97',
    resource='c636e6f7-e1a6-441a-9519-007ef69197e9',
    filename='servicios.csv',
    )
