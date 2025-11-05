from django.contrib import messages
from django.conf import settings


class Bus:
    def __init__(self, request):
        if settings.DEBUG:
            messages.set_level(request, messages.DEBUG)
        self.request = request
        if request.user.is_authenticated:
            self.username = request.user.username
        else:
            self.username = None

    def debug(self, text: str):
        messages.add_message(
            self.request,
            messages.DEBUG,
            text,
            extra_tags='bg-primary text-white',
            )

    def info(self, text: str):
        messages.add_message(
            self.request,
            messages.INFO,
            text,
            extra_tags='bg-info',
            )

    def success(self, text: str):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            text,
            extra_tags='bg-success text-white',
            )

    def warning(self, text: str):
        messages.add_message(
            self.request,
            messages.WARNING,
            text,
            extra_tags='bg-warning',
            )

    def error(self, text: str):
        messages.add_message(
            self.request,
            messages.ERROR,
            text,
            extra_tags='bg-danger text-white',
            )
