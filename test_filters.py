#!/usr/bin/env python

import sys
from inspect import isclass

import pytest

import filters

# ----------------------------------------------------[ Tests for clean_text ]--

CLEAN_TEXT_SAMPLES = {
    "none_value": (None, None),
    "empty_value": ("", None),
    "_u_value": ("_U", None),
    "sanity_check": ("hola", "hola"),
    "singled_quoted": ("'hola'", 'hola'),
    "doubled_quoted": ('"hola"', 'hola'),
    "triple_singled_quoted": ("'''hola'''", 'hola'),
    "triple_doubled_quoted": ('"""hola"""', 'hola'),
    }


@pytest.fixture(params=CLEAN_TEXT_SAMPLES.values(), ids=CLEAN_TEXT_SAMPLES.keys())
def clean_text_sample(request):
    return request.param


def test_clean_text(clean_text_sample):
    input_value, expected_outcome = clean_text_sample
    assert filters.clean_text(input_value) == expected_outcome


# -------------------------------------------------[ Tests for clean_integer ]--


CLEAN_INTEGER_SAMPLES = {
    "none_value": (None, None),
    "empty_value": ("", None),
    "_u_value": ("_U", None),
    "sanity_check": ("3143", 3143),
    "singled_quoted": ("'3144'", 3144),
    "doubled_quoted": ('"3145"', 3145),
    "not_integer": ('hola, mundo', ValueError),
    }


@pytest.fixture(params=CLEAN_INTEGER_SAMPLES.values(), ids=CLEAN_INTEGER_SAMPLES.keys())
def clean_integer_sample(request):
    return request.param


def test_clean_integer(clean_integer_sample):
    input_value, expected_outcome = clean_integer_sample
    if isclass(expected_outcome) and issubclass(expected_outcome, Exception):
        with pytest.raises(expected_outcome):
            filters.clean_integer(input_value)
    else:
        assert filters.clean_integer(input_value) == expected_outcome

# ----------------------------------------------------------[ Test clean URL ]--

CLEAN_URL_SAMPLES = {
    'sanity': ('http://www.python.org/', 'http://www.python.org/'),
    'none_value': (None, None),
    'empty_value': ('', None),
    '_u_value': ('_U', None),
    'invalid_url': ('María tenia un corderito', ValueError),
    }


@pytest.fixture(params=CLEAN_URL_SAMPLES.values(), ids=CLEAN_URL_SAMPLES.keys())
def clean_url_sample(request):
    return request.param


def test_clean_url(clean_url_sample):
    input_value, expected_outcome = clean_url_sample
    if isclass(expected_outcome) and issubclass(expected_outcome, Exception):
        with pytest.raises(expected_outcome):
            filters.clean_url(input_value)
    else:
        assert filters.clean_url(input_value) == expected_outcome


# ------------------------------------------------------[ Tests for slugify ]--

def test_slugify_simple():
    assert filters.slugify("Hola, mundo árbol") == "hola-mundo-arbol"

def test_slugify_hola():
    assert filters.slugify('holá') == 'hola'

def test_slugify_slug():
    assert filters.slugify('hola123') == 'hola123'

def test_slugify_arbol():
    assert filters.slugify('árbol') == 'arbol'


def test_slugify_vocals():
    assert filters.slugify('áéíóúü-ÁÉÍÓÚÜ') == 'aeiouu-aeiouu'


def test_slugify_enies():
    assert filters.slugify('año') == 'anno'
    assert filters.slugify('AÑO') == 'anno'


def test_slugify_parentesis():
    assert filters.slugify('(hola)') == 'hola'


def test_slugify_corchetes():
    assert filters.slugify('[hola]') == 'hola'


def test_slugify_llaves():
    assert filters.slugify('[hola]') == 'hola'


def test_slugify_pipe():
    assert filters.slugify('hola|mundo') == 'hola-mundo'


def test_slugify_space():
    assert filters.slugify('hola mundo') == 'hola-mundo'


def test_slugify_symbols():
    assert filters.slugify('!"#$%&\'*,.') == ''


def test_slugify_plus():
    assert filters.slugify('hola+mundo') == 'hola-mundo'


def test_slugify_hyphen():
    assert filters.slugify('hola-mundo') == 'hola-mundo'


def test_slugify_slash():
    assert filters.slugify('hola/mundo') == 'hola-mundo'


def test_slugify_backslash():
    assert filters.slugify('hola\\mundo') == 'hola-mundo'


def test_slugify_numbers():
    assert filters.slugify('0123456789') == '0123456789'


def test_slugify_lowercase():
    expected = 'abcdefghijklmnnnopqrstuvwxyz'
    assert filters.slugify('abcdefghijklmnñopqrstuvwxyz') == expected


def test_slugify_uppercase():
    expected = 'abcdefghijklmnnnopqrstuvwxyz'
    assert filters.slugify('ABCDEFGHIJKLMNÑOPQRSTUVWXYZ') == expected


def test_slugify_colon():
    assert filters.slugify('hola:mundo') == 'hola-mundo'


def test_slugify_semicolon():
    assert filters.slugify('hola;mundo') == 'hola-mundo'


def test_slugify_angled_brackets():
    assert filters.slugify('<hola mundo>') == 'hola-mundo'


def test_slugify_equals():
    assert filters.slugify('hola=mundo') == 'hola-mundo'


def test_slugify_question_marks():
    assert filters.slugify('¿hola?') == 'hola'


def test_slugify_exclamation_marks():
    assert filters.slugify('¡hola!') == 'hola'


def test_slugify_at():
    assert filters.slugify('hola@mundo') == 'hola-mundo'


def test_slugify_caret():
    assert filters.slugify('hola^mundo') == 'hola-mundo'


def test_slugify_underscore():
    assert filters.slugify('hola_mundo') == 'hola-mundo'


def test_slugify_grave_accent():
    assert filters.slugify('hola`mundo') == 'holamundo'


def test_slugify_equivalency_sign():
    assert filters.slugify('hola~mundo') == 'hola-mundo'


def test_slugify_multiple_hyphens():
    assert filters.slugify('hola-~mundo') == 'hola-mundo'
    assert filters.slugify('hola-------mundo') == 'hola-mundo'
    assert filters.slugify('hola-~-=-_-^-@-mundo') == 'hola-mundo'


def test_slugify_euro():
    assert filters.slugify('23€') == '23-euros'


def test_slugify_ellipsis():
    assert filters.slugify('hola…mundo') == 'hola-mundo'


def test_slugify_ejemplo():
    expected = 'charla-hablamos-bien-los-canarios'
    assert filters.slugify('Charla: ¿Hablamos bien los canarios?') == expected


if __name__ == "__main__":
    pytest.main()
