from django.shortcuts import render

from . import models


def index(request):
    return render(request, 'directorio/index.html', {
        'titulo': 'Directorio',
        'organismos': models.Organismo.objects.filter(ruta='/'),
        })
