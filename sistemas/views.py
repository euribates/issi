#!/usr/bin/env python3

from django.shortcuts import render

from . import models


def index(request, *args, **kwargs):
    sistemas = models.Sistema.objects.all()
    return render(request, 'sistemas/index.html', {
        'titulo': 'Sistemas de información',
        'sistemas': sistemas,
        })
