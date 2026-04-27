from django.contrib import admin

from sistemas import models 


class FamiliaAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "nombre_familia",
        ]
    search_fields = [
        'nombre_familia',
        ]

admin.site.register(models.Familia, FamiliaAdmin)

