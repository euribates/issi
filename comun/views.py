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


def make_chart(color="lime", percent=100):
    angles = [a * 3.6 for a in range(100)]
    assert len(angles) == 100
    rads = [i * math.pi * 2.0 / 360. for i in angles]
    X = [round(math.sin(a)*40, 2) for a in rads]
    Y = [-round(math.cos(a)*40, 2) for a in rads]
    buff = [
        f'<path stroke="{color}" stroke-width="12" fill="none">',
        ' <animate attributeName="d" calcMode="spline" values="',
        ]
    counter = 0
    middle = len(X) // 2
    flags = [0 if index < middle else 1 for index in range(len(X))]
    counter = 0
    for flag, x, y in zip(flags, X, Y):
        buff.append(f'M 0,-40 A 40,40 0 {flag} 1 {x:.2f},{y:.2f};')
        counter += 1
        if counter >= percent:
            break
    buff.append('" dur="0.8s" repeatCount="1" fill="freeze" />')
    buff.append('</path>\n')
    return ''.join(buff)


def doughnut(request, value=76, top=100):
    if top != 100:
        value = int(round(value * 100 / top))
        top = 100
    rads = (76 * math.pi * 2.0 / 360.)
    x = int(round(40 + 28 * math.sin(rads)))
    y = int(round(40 - 28 * math.cos(rads)))
    response = render(request, 'comun/charts/doughnut.svg', {
        'value': value,
        'x': x,
        'y': y,
        'trace': 'off',
        'width': int(round(value / 3.0)),
        'chart': make_chart(percent=76),
        'chart2': make_chart(color="red", percent=32),
        })
    response['Content-Type'] = "image/svg+xml"
    response['Referrer-Policy'] = 'no-referrer'
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response
