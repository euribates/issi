#!/usr/bin/env python3

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

