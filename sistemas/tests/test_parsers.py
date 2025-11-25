#!/usr/bin/env python3

import pytest
from uuid import UUID

from sistemas import parsers


def test_parse_users_single_username():
    expected = [{
        'name': None,
        'login': 'jrodleo',
        'email': 'jrodleo@gobiernodecanarias.org',
        }]
    assert parsers.parse_users('jrodleo') == expected


def test_parse_users_double_username():
    expected = [{
        'name': None,
        'login': 'malosua',
        'email': 'malosua@gobiernodecanarias.org',
        },
        {
        'name': None,
        'login': 'jrodleo',
        'email': 'jrodleo@gobiernodecanarias.org',
        }]
    assert parsers.parse_users('malosua, jrodleo') == expected


def test_parse_users_single_email():
    expected = [{
        'name': None,
        'login': 'jrodleo',
        'email': 'jrodleo@gobiernodecanarias.org',
        }]
    assert parsers.parse_users('jrodleo@gobiernodecanarias.org') == expected


def test_parse_user_full_email():
    expected = [{
        'name': 'Juan Ignacio',
        'login': 'jrodleo',
        'email': 'jrodleo@gobiernodecanarias.org',
        }]
    assert parsers.parse_users('Juan Ignacio <jrodleo@gobiernodecanarias.org>') == expected


def test_parse_users_bad_input():
    with pytest.raises(ValueError):
        parsers.parse_users("I'm Bad! Bad! (Really, rally bad)")


def test_parse_users_void_input():
    assert parsers.parse_users('') == []


def test_parse_juriscan_single_number():
    assert parsers.parse_juriscan('12345') == [12345]


def test_parse_juriscan_double_number():
    assert parsers.parse_juriscan('12345, 85362') == [12345, 85362]
    assert parsers.parse_juriscan('12345  , 85362') == [12345, 85362]
    assert parsers.parse_juriscan('12345,85362') == [12345, 85362]


def test_parse_juriscan_link():
    url = 'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=68976'
    assert parsers.parse_juriscan(url) == [68976]

def test_parse_juriscan_link_multimple():
    url = (
        'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=68976\n'
        'https://www3.gobiernodecanarias.org/juriscan/ficha.jsp?id=37406&from=0&nreg=25&materiasop=AND&materias1=*&materias2=*&rango1=*&rango2=*&titulo=internet&desdeemi=&hastaemi=&ordendesc=IdRango&orden=asc&numdisp=0&tituloAux=internet.'
        )
    assert parsers.parse_juriscan(url) == [68976, 37406]


def test_parse_juriscan_empty():
    assert parsers.parse_juriscan('') == []


def test_parse_uuid():
    expected = UUID('20f5484b-88ae-49b0-8af0-3a389b4917dd')
    assert parsers.parse_uuid('20f5484b-88ae-49b0-8af0-3a389b4917dd') == expected


def test_parse_uuid_empty():
    assert parsers.parse_uuid('') is None


def test_parse_uuid_bad():
    with pytest.raises(ValueError):
        parsers.parse_uuid('María tenía un corderito')


if __name__ == '__main__':
    pytest.main()
