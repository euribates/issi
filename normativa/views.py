from django.shortcuts import render

from . import models


def index(request, *args, **kwargs):
    return render(request, 'normativa/index.html', {
        'titulo': 'Normativa aplicable',
        'normas': models.Norma.objects.all(),
        })
