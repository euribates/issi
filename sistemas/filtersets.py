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
        fields = {
            'nombre': ['icontains'],
            'codigo': ['icontains'],
            'organismo__nombre_organismo': ['icontains'],
            }
