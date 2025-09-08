#!/usr/bin/env python3

from django import forms

from . import models


class SistemaForm(forms.ModelForm):

    class Meta:
        model = models.Sistema
        fields = '__all__'
