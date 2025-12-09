#!/usr/bin/env python3

from django.core.management.base import BaseCommand
from django.core.management import CommandError

from django.conf import settings

from sistemas.models import Tema
from directorio.models import Organismo

DIRECTORY = settings.BASE_DIR / 'caches'
if not DIRECTORY.exists():
    DIRECTORY.mkdir()
    init_module = DIRECTORY / '__init__.py'
    init_module.touch()


LIGHT_GREEN = "\033[1;32m"
END = "\033[0m"

def green(text: str) -> str:
    '''Devuelve el texto en verde.
    '''
    return f'{LIGHT_GREEN}{text}{END}'


CMD_NAME = 'update_caches'
ABOUT    = 'Actualizar ficheros cache de tablas dir3'
EPILOG   = 'ISSI - Inventario de sistemas de información'

HEADER = '''\
#!/usr/bin/env/python3

"""
caches/{filename}

Fichero de datos con una cache para {reason}.

Atención: Este fichero se genera AUTOMATICAMENTE.

NO debe ser modificado a mano.

Cualquier cambio en este fichero se verá sobreescrito cuando se regenere.

Véase el comando ``update_caches`` y el código del mismo
en ``sistemas.management.commands.update_caches``.
"""
'''

def header(filename, reason):
    return HEADER.format(
        filename=filename,
        reason=reason,
        )


class Command(BaseCommand):
    help = ABOUT

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def genera_dir3(self):
        filename = DIRECTORY / 'dir3.py'
        reason = 'pasar de codigo DIR3 a id. del organismo'
        print(f'Generando caches/{filename.name}', end=' ')
        with open(filename, 'w', encoding='utf-8') as output:
            print(header(filename.name, reason), file=output)
            print('reverse_dir3 = {', file=output)
            for o in Organismo.objects.all():
                print(f'    {repr(o.dir3)}: {repr(o.id_organismo)},', file=output)
            print('    }', file=output)
        print(green('[Ok]'))

    def genera_temas(self):
        filename = DIRECTORY / 'temas.py'
        reason = "cachear la tabla de temas"
        print(f'Generando caches/{filename.name}', end=' ')
        with open(filename, 'w', encoding='utf-8') as output:
            print(header(filename.name, reason), file=output)
            print('temas = {', file=output)
            for t in Tema.objects.all():
                print(f'    {repr(t.id_tema)}: {repr(t.nombre_tema)},', file=output)
            print('    }', file=output)
        print(green('[Ok]'))

    def handle(self, *args, **options):
        """Punto de entrada.
        """
        self.genera_dir3()
        self.genera_temas()
