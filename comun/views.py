#!/usr/bin/env python3

import math

from django.shortcuts import render

from sistemas import breadcrumbs

def homepage(request):
    return render(request, "comun/homepage.html", {
        "titulo": "Inventario de sistemas de información",
        'breadcrumbs': breadcrumbs.bc_issi(),
        })

def labo(request):
    return render(request, "comun/labo.html")


def doughnut(request, value=76, top=100):
    if top != 100:
        value = int(round(value * 100 / top))
        top = 100
    long_path = 1 if value > 50 else 0
    angle = (value * 360 / 100.)
    rads = angle * math.pi / 180.
    x = int(round(40 + 28 * math.sin(rads)))
    y = int(round(40 - 28 * math.cos(rads)))


    angles = [i for i in range(0, 361, 6)]
    rads = [i * math.pi * 2.0 / 360. for i in angles]
    X = [round(math.sin(a)*40, 2) for a in rads]
    Y = [-round(math.cos(a)*40, 2) for a in rads]

    response = render(request, 'comun/charts/doughnut.svg', {
        'value': value,
        'x': x,
        'y': y,
        'long_path': long_path,
        'trace': 'off',
        'width': int(round(value / 3.0)),
        'coords': zip(X, Y),
        })
    response['Content-Type'] = "image/svg+xml"
    response['Referrer-Policy'] = 'no-referrer'
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response
