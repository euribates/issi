#!/usr/bin/env python3

from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.conf import settings

from . import models
from . import parsers

from comun.forms import BootstrapForm
from comun.searchers import search_organismos


class ODSFileForm(BootstrapForm, forms.Form):
    archivo = forms.FileField(
        label='Archivo .ODS (LibreOffice Calc)',
        )


class GranTextoForm(BootstrapForm, forms.Form):

    texto = forms.CharField(
        widget=widgets.Textarea(attrs={"cols": "40", "rows": 12}),
        required=False,
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
        widgets = {
            'finalidad': forms.Textarea(attrs={
                'class': "form-control",
                'cols': 80,
                'rows': 5,
                'placeholder': 'Finalidad del sistema'
                }),
            }

    def organismos_filtrados(self, query: str):
        return search_organismos(query)

    def clean_nombre_sistema(self):
        """Validación del nombre del sistema.
        """
        nombre_sistema = self.cleaned_data['nombre_sistema']
        if result := parsers.parse_nombre_sistema(nombre_sistema):
            nombre_sistema = result.value
            self.cleaned_data['nombre_sistema'] = nombre_sistema
        else:
            raise ValidationError(result.error_message.as_html())
        _sistema_previo = (
            models.Sistema
            .objects.filter(nombre_sistema=nombre_sistema)
            .first()
            )
        if _sistema_previo:
            raise ValidationError(
                f"Ya existe un sistema con ese nombre: {_sistema_previo}",
                )
        return nombre_sistema

    def clean_codigo(self):
        """Validación del nombre código del sistema.
        """
        codigo = self.cleaned_data['codigo']
        if result := parsers.parse_codigo_interno(codigo):
            self.cleaned_data['codigo'] = codigo = result.value
        else:
            raise ValidationError(str(result))
        _sistema_previo = models.Sistema.load_sistema_por_codigo(codigo)
        if _sistema_previo:
            raise ValidationError(
                f"Ya existe un sistema con ese código: {_sistema_previo}",
                )
        return codigo


class EditarSistemaForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = [
            'nombre_sistema',
            'codigo',
            'descripcion',
            'url',
            ]

    def _is_diff(self, sistema, field_name) -> dict:
        old_value = getattr(sistema, field_name)
        new_value = self.cleaned_data[field_name]
        if old_value != new_value:
            return { field_name: f'Modificado a {new_value!r}' }
        return {}

    def diff_with(self, sistema) -> dict:
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
        return search_organismos(query)


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

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = f'{usuario.login}@{settings.EMAIL_DOMAIN}'
        if commit:
            usuario.save()
        return usuario

class AltaUsuarioExternoForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Usuario
        fields = [
            'email',
            'nombre',
            'apellidos',
            'empresa',
            ]

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.login = usuario.email
        if commit:
            usuario.save()
        return usuario


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


