#!/usr/bin/env python3

from html import escape
from dataclasses import dataclass
from typing import Any
import textwrap


@dataclass
class ErrorMessage(ValueError):
    code: str
    name: str
    message: str
    context: dict

    def __str__(self) -> str:
        buff = [f'Error {self.code}: {self.name}']
        buff.append(self.message)
        if self.context:
            buff.append('\nVariables de contexto:')
            for _name, _val in self.context.items():
                buff.append(f' - {_name}: {escape(repr(_val))}')
        return '\n'.join(buff)

    def as_html(self):
        '''Descripción del error para mensajes HTML.
        '''
        buff = [
            '<div class="error-message">',
            '<p>',
            f'<code>{self.code}</code>: <b>{self.name}<b>.',
            f'{self.message}',
            '</p>',
            ]
        if self.context:
            buff.append('<hr>')
            buff.append('<p>Contextp:</p>')
            for _name, _val in self.context.items():
                buff.append(f'<p>{_name}: {escape(repr(_val))}</p>')
        buff.append('</div>')
        return '\n'.join(buff)


class BaseError():
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
        message = self.desc
        if value:
            message = self.desc.format(value=escape(repr(value)))
        return ErrorMessage(self.code, self.name, message, context.copy())


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
        err_handler = BaseError(code, name, desc, refs)
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
