#!/usr/bin/env python3

from datetime import timedelta as TimeDelta

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from comun import notificador 
from comun import links
from comun.claves import generate_secret_token


User = get_user_model()

TOKEN_VALID_DAYS = 3


def load_user_by_email(email) -> User|None:
    """Devuelve el usuario con el email indicado, o ``None``.
    """
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


class EmailToken(models.Model):

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'tokens'
        ordering = ['created_at']

    token = models.CharField(
        max_length=20,
        default=generate_secret_token,
        primary_key=True,
        )
    email = models.EmailField(
        max_length=350,
        )
    created_at = models.DateTimeField(
        default=timezone.now,
        )
    valid_for = models.DurationField(
        default=TimeDelta(days=TOKEN_VALID_DAYS),
        )

    def __str__(self) -> str:
        return f'{self.token[:4]}************{self.token[-4:]}'

    @classmethod
    def load_token(cls, pk: str):
        """Obtener un token a partir de su clave primaria.

        Parameters:

            pk (str): Clave primaria del token

        Returns:

            La instancia, si existe el registro correspondiente
            en la base de datos, o ``None`` en caso contrario.
        """
        
        try:
            return cls.objects.get(token=pk)
        except cls.DoesNotExist:
            return None


def send_validation_email(user: User, token: EmailToken):
    host = 'issi.euribates.eu'
    url_reset = f'http://{host}{links.a_reset_password_check(token)}'
    notificador.send_message(
        [user.email],
        '[ISSI] Solicitud de recuperación y cambio de contraseña',
        'comun/email/reset-password.email',
        user=user,
        token=token,
        url_reset=url_reset,
        )
