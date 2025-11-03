#!/usr/bin/env python3

import pytest

import links


def test_link_a_sistemas():
    expected = '/sistemas/'
    assert links.a_sistemas() == expected


def test_link_a_detalle_sistema():
    expected = '/sistemas/sistema/12/'
    assert links.a_detalle_sistema(12) == expected


if __name__ == "__main__":
    pytest.main()
