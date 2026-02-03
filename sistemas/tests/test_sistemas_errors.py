#!/usr/bin/env python3

from uuid import UUID

import pytest

from comum.erros import ErrorMessage
from sistemas.error import errors


def test_EI0001_is_error_message():
    assert isinstance(errors.EI0001(23), ErrorMessage)


def test_EI0001_message():
    expected = 'El fichero CSV solo puede tener'
    assert expected in str(errors.EI0001(23))


def test_EI0001_message_with_num_linea():
    expected = 'n_linea: 111'
    assert expected in str(errors.EI0002(23, n_linea=111))


def test_num_errores_definidos_en_catalogo():
    """Incrementar el número cuando se den de alta más errores.
    """
    assert len(errors) >= 8
    assert 'EI0001' in errors.keys()


def test_EI0010_uuid_no_identificado():
    """Error si se indica un UUID que no está en la BD.
    """
    uuid = '3fd2f422-d767-11f0-a8c3-38d5470ea667'
    expecteds = [
        'Se ha indicado un UUID de sistema:',
        str(UUID(uuid)),
        'que no existe en la base de datos',
        ]
    for expected in expecteds:
        assert expected in str(errors.EI0010(uuid))


def test_EI0011_codigo_duplicado():
    """Error si se intenta dar de alta un código duplicadpo.
    """
    codigo = 'JURICAN'
    expecteds = [
        'Ya existe en la base de datos',
        'un sistema con el codigo indicado:',
        str(codigo),
        ]
    for expected in expecteds:
        assert expected in str(errors.EI0011(codigo))



if __name__ == "__main__":
    pytest.main()
