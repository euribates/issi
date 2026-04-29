#!/usr/bin/env python3

from django import forms
from django.forms import widgets


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
                for name in self.fields
                }
        return {}


# ------------------------------------------[ Formularios genéricos ]--


class LoginForm(BootstrapForm, forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class EstaSeguroForm(BootstrapForm, forms.Form):
    """Formulario para autorizar operaciones críticas.

    Solo será válido si se ha marcado el checkbox.
    """
    seguro = forms.BooleanField(
        required=True,
        initial=False,
        label="Confirme la operación",
        )

