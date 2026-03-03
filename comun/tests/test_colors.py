#!/usr/bin/env python3

import pytest
import re

from comun.colors import Color


def test_create_random_color():
    c = Color.random()
    assert 0 <= c.red < 256
    assert 0 <= c.green < 256
    assert 0 <= c.blue < 256
    assert c == Color(str(c))


def test_inverse_color():
    c = Color(32, 128, 188)
    assert c.inverse() == Color(223, 127, 67)


def test_create_color_from_color():
    old_color = Color('lavenderblush')
    new_color = Color(old_color)
    assert new_color.red == 255
    assert new_color.green == 240
    assert new_color.blue == 245
    assert new_color.alpha is None
    assert str(new_color) == '#FFF0F5'


def test_change_color():
    old_color = Color('magenta')
    new_color = old_color.change(red=33)
    assert new_color != old_color
    assert new_color.red == 33


def test_create_color_using_positional_args():
    assert str(Color(240, 248, 255)) == '#F0F8FF'
    

def test_create_color_using_positional_args_with_alpha():
    assert str(Color(240, 248, 255, 128)) == '#F0F8FF80'
    

def test_create_color_using_named_args():
    assert str(Color(red=240, green=248, blue=255)) == '#F0F8FF'
    

def test_create_color_using_named_args_with_alpha():
    assert str(Color(red=240, green=248, blue=255, alpha=128)) == '#F0F8FF80'
    

def test_create_color_using_name():
    assert str(Color('aliceblue')) == '#F0F8FF'
    

def test_create_color_using_hexvalue():
    c = Color('#F0F8FF')
    assert c.red == 240
    assert c.green == 248
    assert c.blue == 255
    assert c.alpha is None
    

def test_create_color_using_hexvalue_with_alpha():
    c = Color('#F0F8FF80')
    assert c.red == 240
    assert c.green == 248
    assert c.blue == 255
    assert c.alpha == 128
    

def test_color_to_hsl():
    c = Color(123, 66, 88)
    hue, saturation, ligthness = c.to_hsl()
    assert hue == 336.84
    assert saturation == 30.21
    assert ligthness == 37.0


if __name__ == "__main__":
    pytest.main()
