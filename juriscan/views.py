from django.shortcuts import render

from . import models
from sistemas.models import NormaSistema
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
    ficha = models.Juriscan.load_juriscan(num_ficha)
    if not ficha:
        ficha = models.Juriscan.load_or_create(num_ficha)
    sistemas = NormaSistema.objects.filter(num_juriscan=num_ficha)
    return render(request, 'juriscan/ficha_juriscan.html', {
        'titulo': f'Ficha Juriscán número {num_ficha} - {ficha.titulo}',
        'ficha': ficha,
        'sistemas': sistemas,
        'num_sistemas': sistemas.count(),
        'breadcrumbs': bc.ficha_juriscan(num_ficha),
        })

