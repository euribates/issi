#!/usr/bin/env python3

"""
Decoradores y generadores de uso común.
"""

from typing import Any
from typing import Callable
from typing import Iterable, Iterator
from html import escape
import itertools


def agrupa(rows: Iterable, selector: Callable=None) -> dict:
    '''Agrupa una lista de elementos compuestos.

    Los elementos pueden ser tuplas, diccionarios, registros de la base
    de datos, objetos, etc.

    Se puede definir, mediante el parámetro
    ``selector``, un invocable que, a partir del elemento, devuelva la
    clave por la que se quiere agrupar. Si no se indica selector,
    entonces el selector por defecto espera que los elementos sean
    tuplas, listas, o alguna estructura de datos que se pueda acceder
    por un índice, y utiliza el primer valor, es decir el valor
    en el índice :math:`0` para agrupar.

    Ejemplo de uso:

        >>> datos = [('a', 1), ('b', 2), ('a', 3)]
        >>> agrupado = agrupa(datos)
        >>> assert len(agrupado) == 2
        >>> assert agrupado['a'] == [('a', 1), ('a', 3)]
        >>> assert agrupado['b'] == [('b', 2)]

    Parameters:

        rows (Iterable): Sequencia de elementos

    Returns:

        Un diccionario, donde el componente seleccionado con
        el parámetro ``selector`` actua como clave, u el valor
        es una lista de los elementos de la sequencia que corresponden
        con ese valor.
    '''
    result = {}

    if selector is None:

        def selector(row):
            return row[0]

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


def first(iterable: Iterable, condition=lambda x: True, default=None) -> Any:
    """Busca y devuelve el primer elemento de una sequencia.

    Si se especifica una condición, devuelve el primer elemento
    que la cumpla, o ``None`` si ninguno lo cumple. Podemos usar
    el parámetro ``default`` para que nos devuelva otro valor
    en caso de no encontrar el elemento buscado.

    Si no se indica la condición, devuelve el primer elemento
    de la secuencia.

    Si la secuencia está vacia, devuelve ``None``
    o el valor indicado en el parámetro ``default``, si se ha
    especificado.

    Ejemplos:

        >>> assert first(range(10)) == 0
        >>> assert first(range(10), lambda x: x != 0) == 1
        >>> assert first(range(10), lambda x: x>3) == 4
        >>> assert first(range(10), lambda x: x>30, default=-1) == -1

    Parameters:

      iterable (Iterable): Una secuencia de elementos

      condition (Callale): un *callable* que acepta un elemento
        de la secuencia y devulve un booleano.

      defaut (Any): Valor centinela, que se usa para señalizar
        que se ha agotado la secuencia y no se ha encontrado ningún
        elemento de les deseados.  Por defecto es ``None``.


    Returns:

        Any: Si no se espedifica ninguna condición, el primer elemento
        de la secuencia. Si se especifica la condición, el primer
        elemento de la secuencia que la satisfaga. Si la secuencia
        está vacía o ningún elemento cumple la condición, se devuelve
        el valor centinela indicado por el parámetro ``default``,
        por defecto, ``None``.
    """
    for item in iterable:
        if condition(item):
            return item
    return default


def count_if(items: Iterable, condition: Callable) -> int:
    """
    Número de elementos que cumplen una condicion.

    Calcula el número de elementos del iterable para los 
    que la condición es verdadera.

    El parámetro `condición` debe ser un invocable que
    acepta un elemento de la secuencia y devuelva un booleano.

    Ejemplo de uso:

        >>> from comun.seqtools import count_if
        >>> def is_even(num: int) -> bool:
        ...     return item % 2 == 0
        ...
        >>> assert count_if([1, 2, 3, 4], is_even) == 2

    Parameters:

        items (Iterable): Sequencia de elementos.

        condition (Callable): Función que acepta como entrada un
            elemento de la secuencia, y devuelve un booleano
            que indica si debemos contarlo o no.

    Returns:

        int: Número de elementos de la secuencia que cumplen
            la condición indicada.
    """
    return sum(1 for item in items if condition(item))


def split_iter(items: Iterable, condition: Callable) -> tuple[Iterable, Iterable]:
    """
    Divide un iterable en dos, en base a una condición.

    La condición debe ser un invocable que acepte un elemento de la
    secuencia y devuelva un valor booleano. La función ``split_iter``
    devuelve dos iterables: el primero para los elementos que
    ``condition`` evalúa como ``True`` y el segundo para ``False``.

    Ejemplo:

        >>> def is_even(num: int) -> bool:
        ...     return item % 2 == 0
        ...
        >>> pares, impares = split_iter(range(10), is_even)
        >>> assert list(pares) == [0, 2, 4, 6, 8]
        >>> assert list(impares) == [1, 3, 5, 7, 9]

    Es muy habitual usarlo con expresiones *lambda*:

        >>> lt4, gte4 = split_iter(range(10), lambda x: x < 4)
        >>> assert list(lt4) == [0, 1, 2, 3]
        >>> assert list(gte4) == [4, 5, 6, 7, 8, 9]

    Parameters:

        items (Iterable): Sequencia de elementos.

        condition (Callable): Función que acepta como entrada un
            elemento de la secuencia, y devuelve un booleano
            que indica en en cual de los dos iterables
            devuelto debe ir el elemento.

    Returns:
        
        tuple[Iterable, Iterable]: Una dupla de dos iteradores, en el
        primero están los elementos de la secuencia original para los
        que la función de condición devuelve ``True``, y en el segundo
        los elementos para los que devuelve ``False``.
    """
    a_iter, b_iter = itertools.tee(items, 2)
    positive_iter = (_ for _ in a_iter if condition(_))
    negative_iter = (_ for _ in b_iter if not condition(_))
    return positive_iter, negative_iter


def split_list(iterable, condition):
    '''Como split_iter, pero devuelve listas en vez de iterables.

    Esta función se comporta igual que :py:func:`split_iter`, pero
    en vez de devolver una tupla de iteradores, devuelve una tupla
    de listas.

    Parameters:

        items (Iterable): Sequencia de elementos.

        condition (Callable): Función que acepta como entrada un
            elemento de la secuencia, y devuelve un booleano
            que indica en en cual de los dos iterables
            devuelto debe ir el elemento.

    Returns:
        
        tuple[list, list]: Una dupla de dos listas, en la primero están
        los elementos de la secuencia original para los que la función
        de condición devuelve ``True``, y en la segunda los elementos
        para los que devuelve ``False``.

    '''
    positive_items, negative_items = split_iter(iterable, condition)
    return list(positive_items), list(negative_items)


def batch(items: Iterable, size: int=2) -> Iterator[list]:
    """Divide un iterable en una serie de listas más pequeñas.

    Acepta un iterable y lo divide en una serie de listas
    de tamaño fijo, definido con el segundo parámetro, ``size`` (por
    defecto, :math:`2`). Las listas son todas del mismo tamaño, excepto
    la última, que podría tener menos elementos.

    Ejemplo:

    >>> assert list(batch(range(1, 8), 3)) == [(1, 2, 3), (4, 5, 6), (7,)]

    Parameters:

        items (Iterable): Sequencia de elementos.

        size (int): El tamaño de los secciones. Por defecto, 2. La
        última lista podrá tener un número menor de elementos que
        el indicado.

    Returns:

        Iterator[list]: Es un iterador, cada llamada devolverá una lista
        con los ``size`` elementos correspondientes, o puede que menos
        en el caso de la última.

    """
    iterable = iter(items)
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


def static(**kwargs):
    '''Decorador para añadir variables estáticas a una función.

    Todos los parámetros por nombre que se indiquen, con el valor
    correspondiente, se crean como atributos de la propia función.

    El decorador no modifica en ningún otro aspecto a la función.

    Ejemplo de uso:

        >>> @static(base=12)
        ... def suma(offset: int) -> int:
        ...     return suma.base + offset
        ...
        >>> assert suma(3) == 15

    Parameters:

        kwargs(dict): Parámetros pasados por nombre para indicar
            los nombres valores de las variables estáticas
            asociadas a la función decorada

    Returns:

        La misma función sobre la que se aplica, pero con
        atributos adicionales.
    '''
    def _wraped(functor: Callable) -> Callable:
        for key, value in kwargs.items():
            setattr(functor, key, value)
        return functor
    return _wraped
