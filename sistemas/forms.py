#!/usr/bin/env python3

from django import forms
from django.forms import widgets

from . import models

class BaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AltaSistemaForm(forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = [
            'nombre',
            'codigo',
            'organismo',
            'proposito',
            'tema',
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


class EditarSistemaForm(BaseForm):

    class Meta:
        model = models.Sistema
        fields = [
            'nombre',
            'codigo',
            'descripcion',
            'url',
            ]

class AsignarOrganismoForm(BaseForm):

    class Meta:
        model = models.Sistema
        fields = ['organismo']

    def organismos_filtrados(self, query: str):
        return models.Organismo.search_organismos(query)


class AsignarTemaForm(BaseForm):
    class Meta:
        model = models.Sistema
        fields = ['tema']


class AsignarIconoForm(BaseForm):
    class Meta:
        model = models.Sistema
        fields = ['icono']


class EditarPropositoForm(BaseForm):

    class Meta:
        model = models.Sistema
        fields = ['proposito']

    proposito = forms.CharField(
        widget=widgets.Textarea(attrs={"cols": "40", "rows": 12}),
        required=False,
        )


class AsignarResponsableForm(BaseForm):

    class Meta:
        model = models.Perfil
        fields = ['cometido', 'usuario']

    def organismos_filtrados(self, query: str):
        return models.Organismo.search_organismo(query)
