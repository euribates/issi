#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime as DateTime
from urllib.request import urlretrieve

from django.conf import settings

import dataclasses

DIAS_VIGENTE = 15
DATOS_CANARIAS = 'https://datos.canarias.es/catalogos/general'


@dataclasses.dataclass
class OpenData:
    '''Clase de ayuda para consultar el catálogo de datos abiertos.
    '''
    dataset: str
    resource: str
    filename: str

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

    def descargar_datos(self, force=False) -> Path:
        '''Devuelve la ruta del fichero local, actualizado.

        Si la copia local no existe, o si está desfasada (es
        decir, descargada hace más de `DIAS_VIGENTE` días), se
        lee de nuevo desde la fuente.

        Returns: Un objeto de tipo `Path` con la ruta del fichero
                 local.
        '''
        target_file = settings.BASE_DIR / Path(self.filename)
        if target_file.exists():
            stat = target_file.stat()
            mod_date = DateTime.fromtimestamp(stat.st_mtime)
            delta = DateTime.now() - mod_date
            is_still_valid = bool(delta.days <= DIAS_VIGENTE)
            if is_still_valid and not force:  # El fichero local aun es válido
                return target_file
        #  El fichero local tiene que actualizarse
        urlretrieve(self.url(), target_file)
        return target_file


procedimientos = OpenData(
    dataset='946cdcde-2118-48ef-a30a-f9dc812c82db',
    resource='10b71b12-fb77-47b7-88f6-ec46ebee1548',
    filename='procedimientos.csv',
    )

servicios = OpenData(
    dataset='41d56909-566f-4ab2-99e2-78a03577bb97',
    resource='c636e6f7-e1a6-441a-9519-007ef69197e9',
    filename='servicios.csv',
    )
