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
        return (
            models.Organismo.objects.filter(
                Q(nombre_organismo__icontains=query) |
                Q(categoria__icontains=query) |
                Q(dir3__icontains=query)
                )
            )
