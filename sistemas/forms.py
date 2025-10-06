#!/usr/bin/env python3

from django import forms

from . import models


class AltaSistemaForm(forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = [
            'nombre',
            'codigo',
            'organismo',
            'proposito',
            'url',
            'tema',
            'es_transversal',
            'es_subsistema_de',
            ]
