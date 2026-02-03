#!/usr/bin/env python3

from html import escape
from dataclasses import dataclass


@dataclass
class ErrorMessage():

    code: str
    name: str
    message: str
    context: dict

    def __str__(self) -> str:
        '''Descripción del error en texto plano.
        '''
        buff = [f'Error {self.code}: {self.name} ']
        buff.append(self.message)
        if self.context:
            for _name, _val in self.context.items():
                buff.append(f' - {_name}: {escape(repr(_val))}')
        return '\n'.join(buff)

    def as_html(self):
        '''Descripción del error en formato HTML.
        '''
        buff = [
            '<div class="error-message">',
            '<p>',
            f'<code class="codigo-error">{self.code}</code>:'
            f' <b class="nombre-error">{self.name}<b>.',
            f'{self.message}',
            '</p>',
            ]
        if self.context:
            buff.append('<dl>')
            for _name, _val in self.context.items():
                buff.append(f'<dt>{_name}</dt>')
                buff.append(f' <dd>{escape(repr(_val))}</dd>')
            buff.append('</dl>')
        buff.append('</div>')
        return '\n'.join(buff)

    def __call__(self, value=None, **context):
        message = self.message
        if value:
            message = message.format(value=escape(repr(value)))
        return ErrorMessage(
            self.code,
            self.name,
            message,
            context.copy(),
            )


class ErrorCatalog:

    kernel = {}

    def register(self, code, name, desc='', refs=None):
        '''Decorador para registar una clase de error en el catálogo.
        '''
        refs = list(refs) if refs else []
        self.kernel[code] = ErrorMessage(code, name, desc, refs)

    def __len__(self):
        return len(self.kernel)

    def __getattr__(self, name):
        if name in self.kernel:
            return self.kernel[name]
        raise AttributeError(
            'La clase ErrorCatalog no tienen ningún'
            f' atributo llamado {escape(name)}'
            )

    def __getitem__(self, key):
        return self.kernel[key]

    def __iter__(self):
        return iter(list(self.kernel.items()))

    def keys(self):
        '''Devuelve los códigos de errores registrados.
        '''
        return self.kernel.keys()


errors = ErrorCatalog()
