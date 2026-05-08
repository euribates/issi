#!/usr/bin/env python3

from django.db.models import Q

from sistemas.models import Sistema
from directorio.models import Empresa
from directorio.models import Organismo

from sistemas.parsers import parse_uuid

    

def search_empresas(query):
    qs = Empresa.objects.all()
    if query:
        qs = qs.filter(
            Q(nombre_empresa__icontains=query) |
            Q(nif__icontains=query)
            )
    return qs


def search_organismos(query):
    qs = Organismo.objects.all()
    if query:
        qs = qs.filter(
            Q(nombre_organismo__icontains=query) |
            Q(categoria__icontains=query) |
            Q(dir3__istartswith=query)
            )
    return qs


def search_sistemas(query):
    qs = Sistema.objects.select_related('organismo').all()
    if query:
        qs = qs.filter(
            Q(nombre_sistema__icontains=query) |
            Q(codigo__icontains=query) |
            Q(finalidad__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(observaciones__icontains=query) |
            Q(organismo__nombre_organismo__icontains=query) |
            Q(organismo__dir3__istartswith=query) 
            )
        is_uuid = parse_uuid(query)
        if is_uuid.is_success():
            qs = qs | Sistema.objects.filter(uuid_sistema=is_uuid.value)
    return qs


