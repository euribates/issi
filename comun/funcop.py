#!/usr/bin/env python3

"""
## FuncOp - Functional operators

"""

from typing import Callable
from html import escape
import itertools


def agrupa(rows: list, selector: Callable=None) -> dict:
    '''Agrupa una lista de elementos compuestos.

    Los elementos pueden ser tuplas, diccionarios, registros de la base
    de datos, objetos, etc.  Hay que definir mediante el parámetro
    `selector` un _callable_ que, a partir del elemento, devuelva la
    clave por la que se quiere agrupar. Si no se indica selector,
    entonces el selector por defecto espera que los elementos sean
    tuplas, listas, o alguna estructura de datos que se pueda acceder
    por un índice, y utiliza el primer valor, es decir el valor
    en el índice $0$ para agrupar.

    Ejemplo de uso:

        >>> datos = [('a', 1), ('b', 2), ('a', 3)]
        >>> agrupado = agrupa(datos)
        >>> assert agrupado['a'] == [('a', 1), ('a', 3)]
        >>> assert agrupado['b'] == [('b', 2)]
        >>> assert len(agrupado) == 2
    '''
    result = {}
    
    if selector is None:

        def selector(row):
            return _row[0]

    if not callable(selector):
        raise TypeError(
            'El parámetro selector debe ser un invocable:'
            ' una función, en método, una instancia de una'
            ' clase con un metodo `__call__`, etc.'
            f' pero es un {escape(repr(type(selector)))}'
            )
    for row in rows:
        key = selector(row)
        if key in result:
            result[key].append(row)
        else:
            result[key] = [row]
    return result


def first(iterable, condition=lambda x: True, default=None):
    """
    Find and return the first item in the `iterable` that
    satisfies the `condition`.

    Notes:

      - If the condition is not given, returns the first item of
        the iterable. If the iterable is empty, returns the `default`
        value.

    Examples:

        >>> assert first(range(10)) == 0
        >>> assert first(range(10), lambda x: x != 0) == 1
        >>> assert first(range(10), lambda x: x>3) == 4
        >>> assert first(range(10), lambda x: x>30, default=-1) == -1

    Args:

      iterable (iterable): any iterable

      condition (callale): a callable that acceps a item of the
        sequence and returns a boolean

      defaut (Any): default sentinel value to be used in no
        item in the iterable satisfies the condition. Value
        by default is `None`.


    Returns:

        First item on the sequence to satisty the condition, or
        the sentinel value if no one of the items satisfy the
        condition.
    """
    for item in iterable:
        if condition(item):
            return item
    return default


def count_if(iterable, condition):
    """
    Returns the number of elements in iterable where condition is true.

    The `condition` parameter must be a callable expecting an item
    of the sequence, and returning a boolean.

    Example of use:

        >>> from comun.seqtools import count_if
        >>> assert count_if([1, 2, 3, 4], lambda item: item % 2 == 0) == 2
    """
    return sum(1 for item in iterable if condition(item))


def split_iter(iterable, condition):
    """
    Split an iterable in two, based on callable condition.

    condition must be a callable that accepts an element
    of the sequence, and returns a boolean. The `split_iter`
    function returns two iterables: First one is for the items
    that are avaluated by `condition` as `True`, second one is
    an iterable for the rest.

    Example:

        >>> pares, impares = split_iter(range(10), lambda x: x % 2 == 0)
        >>> assert list(pares) == [0, 2, 4, 6, 8]
        >>> assert list(impares) == [1, 3, 5, 7, 9]
        >>> lt4, gte4 = split_iter(range(10), lambda x: x < 4)
        >>> assert list(lt4) == [0, 1, 2, 3]
        >>> assert list(gte4) == [4, 5, 6, 7, 8, 9]
    """
    a, b = itertools.tee(iterable, 2)
    positive_iter = (_ for _ in a if condition(_))
    negative_iter = (_ for _ in b if not condition(_))
    return positive_iter, negative_iter


def split_list(iterable, condition):
    '''Like split_iter, but it returns lists instead of iterables.
    '''
    positive_items, negative_items = split_iter(iterable, condition)
    return list(positive_items), list(negative_items)


def batch(iterable, size=2):
    """Take an iterable and split it in several list
    of size _size_, except for the last one, which
    could have less elements.

    Example:

    >>> assert list(batch(range(1, 8), 3)) == [(1, 2, 3), (4, 5, 6), (7,)]
    """
    iterable = iter(iterable)
    while True:
        chunk = []
        for _ in range(size):
            try:
                chunk.append(next(iterable))
            except StopIteration:
                if chunk:
                    yield tuple(chunk)
                return
        if chunk:
            yield tuple(chunk)
