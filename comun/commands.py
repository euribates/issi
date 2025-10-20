#!/usr/bin/env python3

from dataclasses import dataclass

from django.utils.safestring import mark_safe


@dataclass
class Command:
    url: str
    text: str
    klass: str = 'primary'
    disabled: bool = False

    def __str__(self):
        return mark_safe(
            '<a type="button"'
            f' href="{self.url}"'
            f' class="btn btn-{self.klass}">'
            f'{self.text}'
            '</a>'
            )
