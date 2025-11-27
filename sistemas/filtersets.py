#!/usr/bin/env python3

from django.db.models import Q

import django_filters

from . import models


class UsuarioFilter(django_filters.FilterSet):

    class Meta:
        model = models.Usuario
        fields = {
            'login': ['icontains'],
            'nombre': ['icontains'],
            'apellidos': ['icontains'],
            'organismo__nombre_organismo': ['icontains'],
            }


class SistemaFilter(django_filters.FilterSet):

    class Meta:
        model = models.Sistema
        fields = ['query']

    query = django_filters.CharFilter(method='full_text', label="Search")
    
    def full_text(self, queryset, name, value):
        from icecream import ic; ic(name)
        from icecream import ic; ic(value)
        return queryset.filter(
            Q(nombre_sistema__icontains=value) |
            Q(codigo__icontains=value) |
            Q(organismo__nombre_organismo__icontains=value)
            )


class OrganismoFilter(django_filters.FilterSet):

    class Meta:
        model = models.Organismo
        fields = [
            'nombre_organismo',
            'dir3',
            'categoria',
            ]

    nombre_organismo = django_filters.CharFilter(lookup_expr='icontains')
    dir3 = django_filters.CharFilter(lookup_expr='icontains')


class ActivoFilter(django_filters.FilterSet):

    class Meta:
        model = models.Activo
        fields = [
            'nombre_activo',
            'descripcion',
            'es_prioritario',
            'esta_georeferenciado',
            ]

    nombre_activo = django_filters.CharFilter(lookup_expr='icontains')
    descripcion = django_filters.CharFilter(lookup_expr='icontains')
