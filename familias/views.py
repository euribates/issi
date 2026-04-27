from django.shortcuts import render

from sistemas.models import Familia


def index(request, *args, **kwargs):
    from django.http import HttpResponse
    familias = Familia.objects.with_counts().all()
    return render(request, "familias/index.html", {
        'titulo': 'Familias',
        'familias': familias,
        })
