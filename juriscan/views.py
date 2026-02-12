from django.shortcuts import render

from . import models
from . import breadcrumbs as bc


def index(request):
    juriscan = models.Juriscan.objects.all()
    return render(request, 'juriscan/index.html', {
        'titulo': 'Referencias a Juriscán',
        'juriscan': juriscan,
        'num_juriscan': juriscan.count(),
        'breadcrumbs': bc.juriscan(),
        })


def ficha_juriscan(request, num_ficha: int):
    ficha = models.Juriscan.load_or_create(num_ficha)
    return render(request, 'juriscan/ficha_juriscan.html', {
        'titulo': f'Ficha Juriscán número {num_ficha} - {ficha.titulo}',
        'ficha': ficha,
        'num_sistemas': ficha.sistemas.count(),
        'breadcrumbs': bc.ficha_juriscan(num_ficha),
        })

