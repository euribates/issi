#!/usr/bin/env python3

from django import forms
from django.forms import widgets

from . import models

class SimpleForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            widget = visible.field.widget
            match widget.__class__:
                case widgets.RadioSelect:
                    widget.attrs['class'] = 'form-check-input'
                case widgets.CheckboxInput:
                    widget.attrs['class'] = 'form-check-input'
                case _:
                    widget.attrs['class'] = 'form-control'


# ------------------------------------------[ Formularios genéricos ]--


class EstaSeguroForm(SimpleForm):
    """Formulario para autorizar operaciones críticas.

    Solo será válido si se ha marcado el checkbox.
    """
    seguro = forms.BooleanField(
        required=True,
        initial=False,
        label="Confirme la operación",
        )


class CVSFileForm(SimpleForm):
    archivo =forms.FileField(
        label='Archivo CVS',
        )


# ---------------------------------------[ Formularios para modelos ]--


class BaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            widget = visible.field.widget
            match widget.__class__:
                case widgets.RadioSelect:
                    widget.attrs['class'] = 'form-check-input'
                case widgets.CheckboxInput:
                    widget.attrs['class'] = 'form-check-input'
                case _:
                    widget.attrs['class'] = 'form-control'


class AltaSistemaForm(BaseForm):

    class Meta:
        model = models.Sistema
        fields = [
            'nombre_sistema',
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
            'nombre_sistema',
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


class AsignarFamiliaForm(BaseForm):
    class Meta:
        model = models.Sistema
        fields = ['familia']


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


class EditarDescripcionForm(BaseForm):

    class Meta:
        model = models.Sistema
        fields = ['descripcion']

    descripcion = forms.CharField(
        widget=widgets.Textarea(attrs={"cols": "40", "rows": 12}),
        required=False,
        )


class AsignarResponsableForm(BaseForm):

    class Meta:
        model = models.Perfil
        fields = ['cometido', 'usuario']
        widgets = {
            'cometido': forms.RadioSelect(),
            }


class AsignarInterlocutorForm(BaseForm):

    class Meta:
        model = models.Interlocutor
        fields = ['usuario']


class AltaUsuarioForm(BaseForm):

    class Meta:
        model = models.Usuario
        fields = [
            'login',
            'nombre',
            'apellidos',
            'organismo',
            ]
