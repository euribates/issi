#!/usr/bin/env python3

import math

from django.shortcuts import render

from sistemas import breadcrumbs


PIE_COORDS = [
    (0, 0.0, -40.0), (0, 2.51, -39.92), (0, 5.01, -39.68), (0, 7.5, -39.29),
    (0, 9.95, -38.74), (0, 12.36, -38.04), (0, 14.72, -37.19), (0, 17.03, -36.19),
    (0, 19.27, -35.05), (0, 21.43, -33.77), (0, 23.51, -32.36), (0, 25.5, -30.82),
    (0, 27.38, -29.16), (0, 29.16, -27.38), (0, 30.82, -25.5), (0, 32.36, -23.51),
    (0, 33.77, -21.43), (0, 35.05, -19.27), (0, 36.19, -17.03), (0, 37.19, -14.72),
    (0, 38.04, -12.36), (0, 38.74, -9.95), (0, 39.29, -7.5), (0, 39.68, -5.01),
    (0, 39.92, -2.51), (0, 40.0, -0.0), (0, 39.92, 2.51), (0, 39.68, 5.01),
    (0, 39.29, 7.5), (0, 38.74, 9.95), (0, 38.04, 12.36), (0, 37.19, 14.72),
    (0, 36.19, 17.03), (0, 35.05, 19.27), (0, 33.77, 21.43), (0, 32.36, 23.51),
    (0, 30.82, 25.5), (0, 29.16, 27.38), (0, 27.38, 29.16), (0, 25.5, 30.82),
    (0, 23.51, 32.36), (0, 21.43, 33.77), (0, 19.27, 35.05), (0, 17.03, 36.19),
    (0, 14.72, 37.19), (0, 12.36, 38.04), (0, 9.95, 38.74), (0, 7.5, 39.29),
    (0, 5.01, 39.68), (0, 2.51, 39.92), (1, 0.0, 40.0), (1, -2.51, 39.92),
    (1, -5.01, 39.68), (1, -7.5, 39.29), (1, -9.95, 38.74), (1, -12.36, 38.04),
    (1, -14.72, 37.19), (1, -17.03, 36.19), (1, -19.27, 35.05), (1, -21.43, 33.77),
    (1, -23.51, 32.36), (1, -25.5, 30.82), (1, -27.38, 29.16), (1, -29.16, 27.38),
    (1, -30.82, 25.5), (1, -32.36, 23.51), (1, -33.77, 21.43), (1, -35.05, 19.27),
    (1, -36.19, 17.03), (1, -37.19, 14.72), (1, -38.04, 12.36), (1, -38.74, 9.95),
    (1, -39.29, 7.5), (1, -39.68, 5.01), (1, -39.92, 2.51), (1, -40.0, 0.0),
    (1, -39.92, -2.51), (1, -39.68, -5.01), (1, -39.29, -7.5), (1, -38.74, -9.95),
    (1, -38.04, -12.36), (1, -37.19, -14.72), (1, -36.19, -17.03), (1, -35.05, -19.27),
    (1, -33.77, -21.43), (1, -32.36, -23.51), (1, -30.82, -25.5), (1, -29.16, -27.38),
    (1, -27.38, -29.16), (1, -25.5, -30.82), (1, -23.51, -32.36), (1, -21.43, -33.77),
    (1, -19.27, -35.05), (1, -17.03, -36.19), (1, -14.72, -37.19), (1, -12.36, -38.04),
    (1, -9.95, -38.74), (1, -7.5, -39.29), (1, -5.01, -39.68), (1, -2.51, -39.92),
    (1, -0.01, -40.0)
    ]


def homepage(request):
    return render(request, "comun/homepage.html", {
        "titulo": "Inventario de sistemas de información",
        'breadcrumbs': breadcrumbs.bc_issi(),
        })

def labo(request):
    return render(request, "comun/labo.html")


def make_chart(percent, color='Lime'):
    buff = [
        f'<path stroke="{color}" stroke-width="16" fill="none">',
        ' <animate attributeName="d" calcMode="spline" values="',
        ]
    for counter, coord in enumerate(PIE_COORDS):
        flag, x, y = coord
        buff.append(f'M 0,-40 A 40,40 0 {flag} 1 {x:.2f},{y:.2f};')
        if counter >= percent:
            break
    buff.append('" dur="0.8s" repeatCount="1" fill="freeze" />')
    buff.append('</path>\n')
    return ''.join(buff)


def doughnut(request):

    good = int(request.GET.get('g', 19))
    regular = int(request.GET.get('r', 12))
    bad = int(request.GET.get('b', 7))
    total = bad + regular + good

    red_percent = int(round(bad * 100.0 / total))
    yellow_percent = int(round((bad+regular) * 100.0 / total))
    green_percent = 100
    response = render(request, 'comun/charts/doughnut.svg', {
        'bad': bad,
        'regular': regular,
        'good': good,
        'total': total,
        'green_chart': make_chart(percent=green_percent, color="#00a443"),
        'yellow_chart': make_chart(percent=yellow_percent, color="#f5d80a"),
        'red_chart': make_chart(percent=red_percent, color="#e40405"),
        })
    response['Content-Type'] = "image/svg+xml"
    response['Referrer-Policy'] = 'no-referrer'
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response
