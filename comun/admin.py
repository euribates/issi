from django.contrib import admin
from django.utils import timezone
from comun import models


class EmailTokenAdmin(admin.ModelAdmin):
    list_display = [
        "token",
        "email",
        "created_at",
        "is_valid",
        ]
    list_filter = ['created_at']
    search_fields = [
        'token',
        'email',
        ]

    def is_valid(self, item):
        ahora = timezone.now()
        return ahora > (item.created_at + item.valid_for)

admin.site.register(models.EmailToken, EmailTokenAdmin)
