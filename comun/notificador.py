#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText

from django.template.loader import get_template
from django.conf import settings

from comun.results import Failure, Success
from comun.templatags.comun_filters import as_markdown


def send_message(targets, subject, template, **kwargs):
    """Envía un mensaje de correo a uno o más destinatarios.
    """
    password = settings.EMAIL_PASSWORD
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    sender = settings.EMAIL_USER
    plantilla = get_template(template)
    message_text = plantilla.render(kwargs)
    message = MIMEText(as_markdown(message_text), 'html')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = ', '.join(targets)
    with smtplib.SMTP_SSL(host, port) as smtp_server:
        smtp_server.login(sender, password)
        problems = smtp_server.sendmail(
            sender,
            targets,
            message.as_string(),
            )
        receptores = ', '.join(targets)
        if problems:
            return Failure(
                'Hemos tenido problemas para enviar'
                f' un email a {receptores}'
                )
        return Success(f'Correo enviado a {receptores}')
