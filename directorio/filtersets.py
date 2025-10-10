import django_filters

from . import models


class OrganismoFilter(django_filters.FilterSet):

    class Meta:
        model = models.Organismo
        fields = {
            'nombre_organismo': ['icontains'],
            'dir3': ['icontains'],
            'categoria': ['icontains'],
            }
