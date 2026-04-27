#!/usr/bin/env python3

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Familia
from sistemas import breadcrumbs as bc


def index(request, *args, **kwargs):
    familias = Familia.objects.with_counts().all()
    return render(request, "familias/index.html", {
        'titulo': 'Listado de familias (Áreas temáticas)',
        'breadcrumbs': bc.bc_familias(),
        'tab': 'familias',
        'familias': familias,
        })


@login_required
def detalle_familia(request, familia):
    return render(request, 'familias/detalle-familia.html', {
        'titulo': str(familia),
        'breadcrumbs': bc.bc_detalle_familia(familia),
        'tab': 'familias',
        'familia': familia,
        })




