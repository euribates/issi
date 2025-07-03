from django.contrib import admin

from sistemas.models import Sistema
from sistemas.models import Tema


class SistemaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Sistema, SistemaAdmin)


class TemaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tema, TemaAdmin)
