#!/usr/bin/env python

import pytest

import filters

# Tests for slugify

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
