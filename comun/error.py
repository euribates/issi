#!/usr/bin/env python3

from html import escape
import textwrap


def wrap(texto: str, width=75, indent='  ') -> str:
    return '\n'.join(textwrap.wrap(
        texto, 
        subsequent_indent=indent,
        ))

class Error():
    '''Clase Base para todos los errores.
    '''

    def __init__(self, code, name, desc, refs):
        '''Contructor de la clase Error.
        '''
        self.code = code
        self.name = name
        self.desc = desc
        self.refs = refs or []

    def __call__(self, value=None, **context):
        buff = [f'Error {self.code}: {self.name}']
        desc = self.desc
        if value:
            desc = desc.format(value=escape(repr(value)))
        buff.append(desc)
        if context:
            buff.append('\n--[ Variables de contexto ]--')
            for _name, _val in context.items():
                buff.append(f'- {_name}: {escape(repr(_val))}')
            buff.append('-----------------------------')
        return ValueError('\n'.join(buff))

    def as_resumen_rest(self):
        '''Descripcióm del error para la documentación.
        '''
        desc = self.desc.format(value="**VALUE**")
        buff = [
            f'- ``{self.code}``: **{self.name}**.\n',
            f'  {wrap(desc)}\n'
            ]
        if self.refs:
            buff.append('  Véase:\n')
            for _ref in self.refs:
                buff.append(f'    - :ref:`{_ref}`.')
        return '\n'.join(buff)


class ErrorCatalog:

    kernel = {}

    def register(self, cls):
        '''Decorador para registar una clase de error en el catálogo.
        '''
        code = cls.__name__
        name = cls.name
        desc = cls.desc
        refs = []
        if hasattr(cls, 'refs'):
            refs = list(cls.refs)
        err_handler = Error(code, name, desc, refs)
        self.kernel[code] = err_handler
        return cls

    def __len__(self):
        return len(self.kernel)

    def __getattr__(self, name):
        if name in self.kernel:
            return self.kernel[name]
        raise AttributeError(
            'La clase ErrorCatalog no tienen ningún'
            f' atributo llamado {escape(name)}'
            )

    def __iter__(self):
        self._items = list(self.kernel.items())
        return self

    def __next__(self):
        if self._items:
            return self._items.pop(0)
        raise StopIteration

    def keys(self):
        return self.kernel.keys()


errors = ErrorCatalog()
