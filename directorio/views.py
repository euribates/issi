# from django.shortcuts import render

# from . import models
# from . import breadcrumbs as bc


# def index(request):
    # return render(request, 'directorio/index.html', {
        # 'titulo': 'Directorio',
        # 'subtitulo': 'Organismos de primer nivel (Consejerías y organismos dependientes)',
        # 'organismos': models.Organismo.objects.filter(depende_de=1),
        # 'breadcrumbs': bc.bc_directorio(),
        # })


# def detalle_organismo(request, organismo):
    # return render(request, 'directorio/detalle_organismo.html', {
        # 'titulo': organismo.nombre_organismo,
        # 'breadcrumbs': bc.bc_detalle_organismo(organismo),
        # 'organismo': organismo,
        # 'dependientes': organismo.organismos_dependientes.all(),
        # })




