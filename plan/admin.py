from django.contrib import admin

from plan import models


class BacklogAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'sistema',
        'titulo',
        'estimacion',
        'prioridad',
        'impacto',
        ]
    list_filter = [
        'estimacion',
        'prioridad',
        ]
    search_fields = [
        'titulo',
        'explicacion',
        ]

admin.site.register(models.Backlog, BacklogAdmin)
