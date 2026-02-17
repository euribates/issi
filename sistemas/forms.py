#!/usr/bin/env python3

from django import forms
from django.forms import widgets

from . import models


class BootstrapForm(forms.Form):

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

    def as_dict(self) -> dict:
        if self.is_valid():
            return {
                name: self.cleaned_data[name]
                for name in self.Meta.fields
                }
        return {}


# ------------------------------------------[ Formularios genéricos ]--


class EstaSeguroForm(BootstrapForm, forms.Form):
    """Formulario para autorizar operaciones críticas.

    Solo será válido si se ha marcado el checkbox.
    """
    seguro = forms.BooleanField(
        required=True,
        initial=False,
        label="Confirme la operación",
        )


class CVSFileForm(BootstrapForm, forms.Form):
    archivo =forms.FileField(
        label='Archivo CVS',
        )


# ---------------------------------------[ Formularios para modelos ]--


class AltaSistemaForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = [
            'nombre_sistema',
            'codigo',
            'organismo',
            'finalidad',
            'tema',
            ]

    def organismos_filtrados(self, query: str):
        return models.Organismo.search(query)



class EditarSistemaForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = [
            'nombre_sistema',
            'codigo',
            'descripcion',
            'url',
            ]


class AsignarOrganismoForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['organismo']

    def organismos_filtrados(self, query: str):
        return models.Organismo.search_organismos(query)


class AsignarTemaForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['tema']


class AsignarFamiliaForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['familia']


class AsignarIconoForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['icono']


class EditarFinalidadForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['finalidad']

    finalidad = forms.CharField(
        widget=widgets.Textarea(attrs={"cols": "40", "rows": 12}),
        required=False,
        )


class EditarDescripcionForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['descripcion']

    descripcion = forms.CharField(
        widget=widgets.Textarea(attrs={"cols": "40", "rows": 12}),
        required=False,
        )


class AsignarResponsableForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Perfil
        fields = ['cometido', 'usuario']
        widgets = {
            'cometido': forms.RadioSelect(),
            }


class AsignarInterlocutorForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Interlocutor
        fields = ['usuario']


class AltaUsuarioForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Usuario
        fields = [
            'login',
            'nombre',
            'apellidos',
            'organismo',
            ]


class AltaOpcionForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Opcion
        fields = [
            'texto_opcion',
            'valor',
            ]
        widgets = {
            'texto_opcion': forms.Textarea(attrs={
                'class': "form-control",
                'cols': 70,
                'rows': 7,
                }),
        }

    def save(self, pregunta, commit=True):
        instance = super().save(commit=False)
        instance.pregunta = pregunta
        instance.orden = instance.get_next_orden()
        instance = super().save(commit=commit)
        return instance
