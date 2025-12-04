#!/usr/bin/env python3

import pytest

from sistemas.error import errors


def test_EI0001_is_exception():
    assert isinstance(errors.EI0001(23), ValueError)


def test_EI0001_message():
    expected = 'El fichero CSV solo puede tener'
    assert expected in str(errors.EI0001(23))


def test_EI0001_message_with_num_linea():
    expected = 'n_linea: 111'
    assert expected in str(errors.EI0002(23, n_linea=111))


def test_num_errores_definidos_en_catalogo():
    """Incrementar el número cuando se den de alta más errores.
    """
    assert len(errors) >= 6
    assert 'EI0001' in errors.keys()


if __name__ == "__main__":
    pytest.main()
