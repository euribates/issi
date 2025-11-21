#!/usr/bin/env python3

import pytest

from sistemas import parsers


def test_parse_user_single_username():
    expected = {
        'name': None,
        'login': 'jrodleo',
        'email': 'jrodleo@gobiernodecanarias.org',
        }
    assert parsers.parse_user('jrodleo') == expected


def test_parse_user_single_email():
    expected = {
        'name': None,
        'login': 'jrodleo',
        'email': 'jrodleo@gobiernodecanarias.org',
        }
    assert parsers.parse_user('jrodleo@gobiernodecanarias.org') == expected


def test_parse_user_full_email():
    expected = {
        'name': 'Juan Ignacio',
        'login': 'jrodleo',
        'email': 'jrodleo@gobiernodecanarias.org',
        }
    assert parsers.parse_user('Juan Ignacio <jrodleo@gobiernodecanarias.org>') == expected


def test_parse_user_bad_input():
    with pytest.raises(ValueError):
        parsers.parse_user("I'm Bad! Bad! (Really, rally bad)")


def test_parse_user_void_input():
    assert parsers.parse_user('') is None


if __name__ == '__main__':
    pytest.main()
