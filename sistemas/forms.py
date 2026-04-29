#!/usr/bin/env python3

from django import forms
from django.forms import widgets

from . import models
from comun.forms import BootstrapForm


class ODSFileForm(BootstrapForm, forms.Form):
    archivo = forms.FileField(
        label='Archivo .ODS (LibreOffice Calc)',
        )


class GranTextoForm(BootstrapForm, forms.Form):

    texto = forms.CharField(
        widget=widgets.Textarea(attrs={"cols": "40", "rows": 12}),
        required=False,
        )

    def __init__(selt, texto_inicial='', **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = dict()
        kwargs['initial']['texto'] = texto_inicial
        super().__init__(**kwargs)

    def get_texto(self):
        return self.cleaned_data['texto']


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

    def _is_diff(self, sistema, field_name):
        old_value = getattr(sistema, field_name)
        new_value = self.cleaned_data[field_name]
        if old_value != new_value:
            return { field_name: f'Modificado a {new_value!r}' }
        return {}


    def diff_with(self, sistema):
        result = dict()
        result.update(self._is_diff(sistema, 'nombre_sistema'))
        result.update(self._is_diff(sistema, 'codigo'))
        result.update(self._is_diff(sistema, 'descripcion'))
        result.update(self._is_diff(sistema, 'url'))
        return result



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


class EditarCodigoForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['codigo']


class EditarNombreForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['nombre_sistema']


class EditarURLForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = ['url']


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


class EditarUsuarioForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Usuario
        fields = [
            'nombre',
            'apellidos',
            'organismo',
            'login',
            'email',
            ]


class AltaUsuarioInternoForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Usuario
        fields = [
            'login',
            'nombre',
            'apellidos',
            'organismo',
            ]


class AltaUsuarioExternoForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Usuario
        fields = [
            'login',
            'nombre',
            'apellidos',
            'email',
            'empresa',
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

    def __init__(self, *args, **kwargs):
        self.pregunta = kwargs.pop('pregunta')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.pregunta = self.pregunta
        instance.orden = instance.get_next_orden()
        instance = super().save(commit=commit)
        return instance


class NormativaForm(forms.Form):

    id_juriscan = forms.IntegerField()


