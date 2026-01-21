#!/usr/bin/env python3

import pytest

# Tests para la función agrupa

from comun.funcop import agrupa
from comun.funcop import static
from comun.funcop import first

def test_first_empty_list():

    assert first([]) is None


def test_first_one_element_list():
    assert first([0]) == 0


def test_first_many_element_list():
    assert first([4, 5, 6, 7]) == 4


def test_first_many_element_list_with_condition():
    assert first([4, 5, 6, 7], lambda x: x > 5) == 6


def test_first_many_element_found_nothing():
    assert first([4, 5, 6, 7], lambda x: x > 55) is None


def test_first_many_element_with_sentinel():
    assert first([4, 5, 6, 7], lambda x: x > 55, default=-1) == -1


def test_simple():
    datos = [('a', 1), ('b', 2), ('a', 3)]
    agrupado = agrupa(datos)
    assert agrupado['a'] == [('a', 1), ('a', 3)]
    assert agrupado['b'] == [('b', 2)]
    assert len(agrupado) == 2


def test_with_dataclasses():
    from dataclasses import dataclass

    @dataclass(order=True, frozen=True)
    class Dato:
        count: int
        letter: str
    
    datos = [
        Dato(1, 'a'),
        Dato(2, 'b'),
        Dato(3, 'a'),
        ]
    agrupado = agrupa(datos, selector=lambda _r: _r.letter)
    assert agrupado['a'] == [Dato(1, 'a'), Dato(3, 'a')]
    assert agrupado['b'] == [Dato(2, 'b')]
    assert len(agrupado) == 2


def test_static_decorator():

    @static(base=12)
    def suma(offset: int) -> int:
        return suma.base + offset

    assert suma(3) == 15
    assert suma(-5) == 7
    assert suma(0) == 12


if __name__ == "__main__":
    pytest.main()
