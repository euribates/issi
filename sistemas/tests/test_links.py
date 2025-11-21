#!/usr/bin/env python3

import pytest

import links


def test_link_a_sistemas():
    expected = '/sistemas/'
    assert links.a_sistemas() == expected


def test_link_a_detalle_sistema():
    expected = '/sistemas/sistema/12/'
    assert links.a_detalle_sistema(12) == expected


def test_link_a_activos():
    expected = '/sistemas/activos/'
    assert links.a_activos() == expected


def test_link_a_conmutar_campo():
    expected = '/sistemas/sistema/1832/conmutar/es_prioritario/'
    assert links.a_conmutar_campo(1832, 'es_prioritario') == expected


def test_link_a_familias():
    expected = '/sistemas/familias/'
    assert links.a_familias() == expected


def test_link_a_detalle_familia():
    expected = '/sistemas/familias/F01/'
    assert links.a_detalle_familia('F01') == expected


def test_link_a_exportar_sistemas():
    expected = '/sistemas/exportar/'
    assert links.a_exportar_sistemas() == expected


def test_link_a_usuarios():
    expected = '/sistemas/usuario/'
    assert links.a_usuario() == expected


def test_link_a_alta_usuario():
    expected = '/sistemas/usuario/alta/'
    assert links.a_alta_usuario() == expected


if __name__ == "__main__":
    pytest.main()
