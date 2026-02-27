#!/usr/bin/env python3

import pytest

from comun.colors import Color


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
