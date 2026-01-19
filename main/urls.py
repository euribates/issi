#!/usr/bin/env python3

import functools

from django.conf import settings
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from comun.views import homepage, labo


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


def goto(url):
    return functools.partial(redirect, url)


urlpatterns = [
    tie("", homepage),
    path("health/", include("health_check.urls")),
    path("favicon.ico", goto('static/favicon.png')),
    path('labo/', labo),
    path("comun/", include('comun.urls')),
    path("glosario/", include('glosario.urls')),
    path("normativa/", include('normativa.urls')),
    path("sistemas/", include('sistemas.urls')),
    path("directorio/", include('directorio.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
        show_indexes=True,
        )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
        show_indexes=True,
        )
