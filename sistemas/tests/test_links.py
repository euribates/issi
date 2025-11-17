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


if __name__ == "__main__":
    pytest.main()
