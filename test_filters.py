#!/usr/bin/env python

import pytest

import filters

def test_slugify_simple():
    assert filters.slugify("Hola, mundo árbol") == "hola-mundo-arbol"


if __name__ == "__main__":
    pytest.main()
