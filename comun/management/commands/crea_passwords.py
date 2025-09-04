#!/usr/bin/env python3

import argparse
import random

from django.core.management.base import BaseCommand

from . import letter_frequencies

CMD_NAME = 'crea_passwords'
ABOUT    = 'Crea una o varias contraseñan pronunciables'
EPILOG   = 'ISSI - Inventario de sistemas de información'

ALFABETO = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS  = r'0123456789'
SYMBOLS  = r'/\#@:][}{*+-=&%|.;,'

DEFAULT_NUM_PASSWORDS = 1
DEFAULT_LEN_PASSWORD = 24
DEFAULT_NUM_DIGITS    = 4
DEFAULT_NUM_SYMBOLS   = 3
DEFAULT_USE_1337      = True

MAP_1337 = {
    'a': ['4', '@'],
    'b': ['8', '|3'],
    'c': ['(', '<', '['],
    'd': ['|)'],
    'e': ['3', ],
    'f': ['|='],
    'g': ['9', '&'],
    'h': ['|-|', '#'],
    'i': ['1', '|', ':', '!'],
    'o': ['0', '[]', '*', '{}'],
    's': ['5', '~'],
    't': ['7', '+'],
    'u': ['|_|'],
    'z': ['2',],
    'w': ['vv', 'vV', 'Vv', 'VV'],
    }

def alter_case(c):
    if random.random() >= 0.65:
        return c.upper()
    return c


def trace(msg, buffer):
    indent = ' ' * (24 - len(msg))
    label = ''.join(buffer)
    print(f'{indent}\x1b[37m{msg}\x1b[0m: \x1b[97m{label}\x1b[0m')


def tron(msg, buffer):
    indent = ' ' * (24 - len(msg))
    label = ''.join(buffer)
    print(f'{indent}\x1b[32m{msg}\x1b[0m: \x1b[92m{label}\x1b[0m')


def troff(msg, buffer):
    indent = ' ' * (24 - len(msg))
    label = ''.join(buffer)
    print(f'{indent}\x1b[31m{msg}\x1b[0m: \x1b[91m{label}\x1b[0m')

class Command(BaseCommand):
    '''Generador de contraseñas pronunciables.
    '''
    help = ABOUT

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs['epilog'] = EPILOG
        return super().create_parser(prog_name, subcommand, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '-n', '--num',
            help='Número de contraseñas a generar',
            type=int,
            default=DEFAULT_NUM_PASSWORDS,
            )
        parser.add_argument(
            '-d', '--digits',
            help='Número mínimo de dígitos en la contraseña',
            type=int,
            default=DEFAULT_NUM_DIGITS,
            )
        parser.add_argument(
            '-s', '--symbols',
            help='Número de caracteres no alfanumericos en la contraseña',
            type=int,
            default=DEFAULT_NUM_SYMBOLS,
            )
        parser.add_argument(
            '-x', '--use_1337',
            action='store_false',
            help='Usar 1337',
            default=DEFAULT_USE_1337,
            )
        parser.add_argument(
            '-l', '--len',
            help='Número total de caracteres en la contraseña',
            type=int,
            default=DEFAULT_LEN_PASSWORD,
            )

    def handle(self, *args, **options):
        num_passwords = options.get('num', DEFAULT_NUM_PASSWORDS)
        for password in range(num_passwords):
            password = self.gen_password(options)
            trace('Password', password)
        
    def gen_password(self, options):
        verbosity = options.get('verbosity')
        len_password = options.get('len', DEFAULT_LEN_PASSWORD)
        num_digits = options.get('digits', DEFAULT_NUM_DIGITS)
        num_symbols = options.get('symbols', DEFAULT_NUM_SYMBOLS)
        use_1337 = options.get('use_1337', DEFAULT_USE_1337)
        _letter = random.choice(ALFABETO)
        buffer = [_letter]
        size = len(buffer)
        for _ in range(len_password - num_digits - num_symbols):
            fraqs = letter_frequencies.FREQS[_letter]
            population = [_[0] for _ in fraqs]
            cum_weights = [_[1] for _ in fraqs]
            _letter = random.choices(population, cum_weights=cum_weights)[0]
            buffer.append(_letter)
            size += 1
        if verbosity > 1:
            tron('Forma pronunciable', buffer)
        if use_1337:
            for index, target in enumerate(buffer):
                if target in MAP_1337 and random.random() < 0.4:
                    reemplazo = random.choice(MAP_1337[target])
                    buffer[index:index+1] = list(reemplazo)
                    for c in reemplazo:
                        if c.isnumeric():
                            num_digits -= 1
                        else:
                            num_symbols -= 1
                    size += len(reemplazo)
            if verbosity > 1:
                tron('1337 code', buffer)
        else:
            if verbosity > 1:
                troff('1337 code disabled', buffer)
        if num_digits > 0:
            size = len(buffer)
            for _ in range(num_digits):
                _number = random.choice(NUMBERS)
                position = random.choice(range(size+1))
                buffer.insert(position, _number)
                size += 1
            if verbosity > 1:
                tron(f'Add {num_digits} digits', buffer)
        else:
            if verbosity > 1:
                troff('No more digits needed', buffer)
        if num_symbols > 0:
            size = len(buffer)
            for _ in range(num_symbols):
                _symbol = random.choice(SYMBOLS)
                position = random.choice(range(size+1))
                buffer.insert(position, _symbol)
                size += 1
            if verbosity > 1:
                tron(f'Add {num_symbols} symbols', buffer)
        else:
            if verbosity > 1:
                troff('No more symbols needed', buffer)
        buffer = [alter_case(c) for c in buffer]
        if verbosity > 1:
            tron(f'Swap case', buffer)
        password = ''.join(buffer)
        return password
