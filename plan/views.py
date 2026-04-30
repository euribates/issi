#!/usr/bin/env python

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from omnibus.bus import Bus
from sistemas import links
from sistemas import breadcrumbs as bc
from comun.forms import EstaSeguroForm
from plan.forms import TareaForm


@login_required
def index(request):
    return render(request, 'plan/index.html')


@login_required
def detalle_tarea(request, tarea):
    return render(request, 'plan/detalle-tarea.html', {
        'titulo': 'Detalles de la la tarea #{tarea.pk}',
        'subtitulo': str(tarea),
        'breadcrumbs': bc.bc_detalle_tarea(tarea),
        'tarea': tarea,
        })


@login_required
def editar_tarea(request, tarea):
    sistema = tarea.sistema
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea, sistema=sistema)
        if form.is_valid():
            tarea = form.save()
            sistema.touch()
            Bus(request).pub_tarea_modificada(tarea)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = TareaForm(
            instance=tarea,
            sistema=sistema,
            )
    return render(request, 'plan/editar-tarea.html', {
        'titulo': f'Editar tarea #{tarea}',
        'subtitulo': str(sistema),
        'breadcrumbs': bc.bc_editar_tarea(tarea),
        'tab': 'sistemas',
        'sistema': sistema,
        'tarea': tarea,
        'form': form,
        })


def cerrar_tarea(request, tarea):
    if request.method == "POST":
        form = EstaSeguroForm(request.POST)
        if form.is_valid():
            tarea.archive()
            Bus(request).pub_tarea_cerrada(tarea)
            return redirect(links.a_detalle_sistema(tarea.sistema.pk))
    else:
        form = EstaSeguroForm()
    return render(request, 'plan/cerrar-tarea.html', {
        'titulo': f'Cerrar la tarea #{tarea.pk}: {tarea.titulo}',
        'breadcrumbs': bc.bc_cerrar_tarea(tarea),
        'tab': 'sistemas',
        'form': form,
        'tarea': tarea,
        })
