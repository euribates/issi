#!/usr/bin/env python3

from django.shortcuts import render


def homepage(request):
    return render(request, "comun/homepage.html", {
        "titulo": "Inventrio de sistemas de información",
        })
