#!/usr/bin/env python

import re


_TABLA_SLUG = ''.maketrans({
    'á': 'a',
    'é': 'e',
    'í': 'i',
    'ó': 'o',
    'ú': 'u',
    'ü': 'u',
    'ñ': 'nn',
    'Á': 'a',
    'É': 'e',
    'Í': 'i',
    'Ó': 'o',
    'Ú': 'u',
    'Ü': 'u',
    'Ñ': 'nn',
    })



def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    text = text.translate(_TABLA_SLUG)
    return text


def clean_text(text:str) -> str:
    if text[0] == text[-1] == '"':
        return text[1:-1]
    return text


def clean_integer(text: str) -> int|None:
    if text is None or text == '' or text == '_U':
        return None
    return int(text)
