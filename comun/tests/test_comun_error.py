#!/usr/bin/env python3

import pytest

from comun.error import ErrorCatalog, ErrorMessage
from comun.error import errors


@pytest.fixture
def catalog():
    '''Sandbox catalog for tests.
    '''
    _catalog = ErrorCatalog()
    _catalog.register('INT01', 'Error interno 1', 'Texto del primer error')
    _catalog.register('INT02', 'Error interno 2', 'Mensaje con valor {value}')
    return _catalog


def test_error_catalog_long(catalog):
    assert len(catalog) == 2


def test_error_catalog_keys(catalog):
    assert list(catalog.keys()) == ['INT01', 'INT02']


def test_error_catalog_as_dict_or_attributes(catalog):
    '''El catálogo se puede acceder como atributo o como clave.
    '''
    assert catalog.INT01 == catalog['INT01']
    assert catalog.INT02 == catalog['INT02']


def test_errors_are_error_message_instances(catalog):
    assert isinstance(catalog.INT01(), ErrorMessage)
    assert isinstance(catalog.INT02(23), ErrorMessage)


def test_error_message_code(catalog):
    err = catalog.INT01()
    assert err.code == 'INT01'


def test_error_message_name(catalog):
    err = catalog.INT01()
    assert err.name == 'Error interno 1'


def test_error_message_message(catalog):
    err = catalog.INT01()
    assert err.message == 'Texto del primer error'


def test_error_message_message_with_value(catalog):
    err = catalog.INT02(744)
    assert err.message == 'Mensaje con valor 744'


def test_error_message_with_extra_context(catalog):
    err = catalog.INT01(filename='stdin', n_linea=32)
    assert err.context == {
        'n_linea': 32,
        'filename': 'stdin'
        }


def test_error_catalog_is_iterable(catalog):
    for name, item in catalog:
        assert name in {'INT01', 'INT02'}
        assert isinstance(item, ErrorMessage)


# ----------------------------------------------[ SSI errores ]--


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
        uuid,
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
        'un sistema con el código indicado:',
        str(codigo),
        ]
    for expected in expecteds:
        assert expected in str(errors.EI0011(codigo))


if __name__ == "__main__":
    pytest.main()
