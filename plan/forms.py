from django import forms

from comun.forms import BootstrapForm
from plan.models import Backlog

class TareaForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = Backlog
        fields = [
            'titulo',
            'explicacion',
            'estimacion',
            'prioridad',
            ]
        widgets = {
            'explicacion': forms.Textarea(attrs={
                'class': "form-control",
                'cols': 70,
                'rows': 5,
                }),
        }

    def __init__(self, *args, **kwargs):
        self.sistema = kwargs.pop('sistema')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.sistema = self.sistema
        instance = super().save(commit=commit)
        return instance
