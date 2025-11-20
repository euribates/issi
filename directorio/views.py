from django.shortcuts import render

from . import models
from . import breadcrumbs as bc


def index(request):
    return render(request, 'directorio/index.html', {
        'titulo': 'Directorio',
        'organismos': models.Organismo.objects.filter(ruta='/'),
        'breadcrumbs': bc.directorio(),
        })


def detalle_organismo(request, organismo):
    return render(request, 'directorio/detalle_organismo.html', {
        'titulo': organismo.nombre_organismo,
        'breadcrumbs': bc.detalle_organismo(organismo),
        'organismo': organismo,
        'dependientes': organismo.organismos_dependientes.all(),
        })



def estudio_organismo(request, organismo):
    return render(request, 'directorio/estudio_organismo.html', {
        'titulo': f'Informe {organismo.nombre_organismo}',
        'breadcrumbs': bc.estudio_organismo(organismo),
        'organismo': organismo,
        'dependientes': organismo.organismos_dependientes.all(),
        'jerarquia': list(organismo.iter_jerarquia()),
        })
