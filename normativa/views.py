from django.shortcuts import render

from . import models
from . import breadcrumbs as bc

def index(request, *args, **kwargs):
    return render(request, 'normativa/index.html', {
        'titulo': 'Normativa aplicable',
        'breadcrumbs': bc.at_normativa(),
        'normas': models.Norma.objects.all(),
        })
