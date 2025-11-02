#!/usr/bin/env python3

from functools import lru_cache

from django import forms
from django.db.models import Q

from . import models


class AltaSistemaForm(forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = [
            'nombre',
            'codigo',
            'organismo',
            'proposito',
            ]

    def organismos_filtrados(self, query: str):
        return models.Organismo.search(query)

    def as_dict(self) -> dict:
        if self.is_valid():
            return {
                name: self.cleaned_data[name]
                for name in self.Meta.fields
                }
        return {}


@lru_cache
def get_choice_temas() -> list[tuple[str, str]]:
    '''Devuelve la lista de temas como tupla código/valor.
    '''
    return [
        (_.id_tema, _.nombre_tema)
        for _ in models.Tema.objects.all()
        ]


class AsignarTemaForm(forms.Form):
    tema = forms.ChoiceField(choices=get_choice_temas)
