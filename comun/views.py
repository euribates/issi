#!/usr/bin/env python3

from django.shortcuts import render

from sistemas import breadcrumbs

def homepage(request):
    return render(request, "comun/homepage.html", {
        "titulo": "Inventario de sistemas de información",
        'breadcrumbs': breadcrumbs.bc_issi(),
        })
