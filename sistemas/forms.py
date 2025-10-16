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
