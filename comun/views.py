#!/usr/bin/env python3

from collections import Counter

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.urls import reverse_lazy

from comun import forms
from comun.models import EmailToken
from comun.models import load_user_by_email, send_validation_email
from sistemas import breadcrumbs
from sistemas import links
from sistemas.models import Sistema
from sistemas.models import Activo
from sistemas.models import Tema
from sistemas.models import Familia
from sistemas.models import Usuario
from directorio.models import Organismo

from comun.graficas import PolarChart
from comun.graficas import Doughnut


def get_stats_sistemas() -> dict:
    """Devuelve las estadísiticas más significativas.
    """
    stats = Counter()
    for s in Sistema.objects.all():
        stats[s.get_estado()] += 1
        stats['sistemas'] += 1
    stats['activos'] = Activo.objects.count()
    stats['usuarios'] = Usuario.objects.count()
    stats['organismos'] = Organismo.objects.count()
    stats['temas'] = Tema.objects.count()
    stats['familias'] = Familia.objects.count()
    return stats



def homepage(request):
    """Página de inicio.
    """
    stats = get_stats_sistemas()
    return render(request, "comun/homepage.html", {
        "titulo": "Inventario de sistemas de información",
        'breadcrumbs': breadcrumbs.bc_issi(),
        "stats": stats,
        "sistemas_chart": Doughnut(
            good=stats['green'],
            regular=stats['yellow'],
            bad=stats['red'],
            width=128,
            height=128,
            ),
        })


def labo(request):
    from comun.charts import BarChart

    chart = BarChart()
    chart.add_value(37, 'rojo', '#F23A20')
    chart.add_value(137, 'verde', '#3AF220')
    chart.add_value(37, 'verde', '#3F22FA')

    polar = PolarChart('ISD', max_value=25)
    polar.add_axis('C', 'Calidad')
    polar.add_axis('D')
    polar.add_axis('I')
    polar.add_axis('P')
    polar.add_axis('R')
    polar.add_axis('S')
    polar.add_serie(
        [12.4, 17.4, 7.0, 1.3, 9.1, 17.4],
        label='ISSI',
        )
    polar.add_serie(
        [18, 14.4, 9.0, 14.3, 7.1, 15.4],
        label='Media',
        )
    
    return render(request, "comun/labo.html", {
        'titulo': 'Esto es una página de pruebas',
        'subtitulo': 'Si ves cosas raras, es normal',
        'chart': chart.as_json(),
        'polar': polar,
        })


def logout_view(request):
    """Cerrar sesión.
    """
    logout(request)
    return redirect('/intranet/')


def login_view(request):
    """Identificación como usuario del sistema.
    """
    next_url = request.GET.get('next', links.a_sistemas())
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
    else:
        form = forms.LoginForm()
    return render(request, 'comun/login.html', context={
        'titulo': 'Validación de usuario',
        'form': form,
        })


def reset_password_ok(request, *args, **kwargs):
    from django.http import HttpResponse
    return HttpResponse("reset_password_ok no implementado", content_type="text/plain")


def reset_password_error(request, *args, **kwargs):
    from django.http import HttpResponse
    return HttpResponse("reset_password_error no implementado", content_type="text/plain")


def reset_password_check(request, token: str, **kwargs):
    from django.http import HttpResponse
    _token = EmailToken.load_token(token)
    return HttpResponse(
        "reset_password_check no implementado. token={_token}",
        content_type="text/plain",
        )



def reset_password(request):
    """Página para recuperar y cambiar la contraseña del usuario.
    """
    if request.method == 'POST':
        form = forms.EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if user := load_user_by_email(email):
                token = EmailToken(email=email)
                token.save()
                send_validation_email(user=user, token=token)
                return redirect(reverse_lazy('comun:reset_password_ok'))
            else:
                return redirect(reverse_lazy('comun:reset_password_error'))
    else:
        form = forms.EmailForm()
    return render(request, 'comun/reset-password.html', {
        'titulo': "Solicitud de recuperación de contraseña",
        'form': form,
        })
