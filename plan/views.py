#!/usr/bin/env python

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from omnibus.bus import Bus
from sistemas import forms
from sistemas import links
from sistemas import breadcrumbs as bc


@login_required
def index(request):
    return render(request, 'backlog/index.html')


@login_required
def editar_backlog(request, backlog):
    sistema = backlog.sistema
    if request.method == 'POST':
        form = forms.BacklogForm(
            request.POST,
            instance=backlog,
            sistema=sistema,
            )
        if form.is_valid():
            backlog = form.save()
            sistema.touch()
            Bus(request).pub_backlog_modificado(backlog)
            return redirect(links.a_detalle_sistema(sistema.pk))
    else:
        form = forms.BacklogForm(
            instance=backlog,
            sistema=sistema,
            )
    return render(request, 'plan/editar-backlog.html', {
        'titulo': f'Editar {backlog} de {sistema}',
        'breadcrumbs': bc.bc_editar_backlog(backlog),
        'tab': 'sistemas',
        'sistema': sistema,
        'backlog': backlog,
        'form': form,
        })
