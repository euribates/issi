#!/usr/bin/env python3

from dataclasses import dataclass

from django.utils.safestring import mark_safe


@dataclass(frozen=True)
class CommandItem:

    url : str
    text : str
    klass : str = 'primary'
    icon : str = ''

    def __str__(self):
        return mark_safe(
          f'<a class="nav-link {{ self.klass }}" aria-current="page"'
          f' href="{self.url}">'
          f'{self.icon} {self.text}'
          '</a>'
          )


class Commands:

    def __init__(self, name, url, klass='nav-link'):
        self.name = name
        self.url = url
        self.klass = klass
        self.menu = []

    def __iter__(self):
        for item in self.menu:
            yield item

    def add(self, url, text, klass, icon):
        self.menu.append(CommandItem( url, text, klass, icon))
        return self

