#!/usr/bin/env python3

import pytest

# Tests para la función agrupa

from comun.funcop import agrupa


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



if __name__ == "__main__":
    pytest.main()
