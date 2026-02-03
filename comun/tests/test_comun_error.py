#!/usr/bin/env python3

import pytest

from comun.error import ErrorCatalog, ErrorMessage


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


if __name__ == "__main__":
    pytest.main()
