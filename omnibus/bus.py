#!/usr/bin/env python3

from html import escape

from django.db.models import Model
from django.contrib import messages

from comun.templatetags.comun_filters import as_markdown
from omnibus.models import Evento


class Bus:

    def __init__(self, request, messages_system=messages):
        assert request.user.is_authenticated
        self.request = request
        self.username = request.user.username
        self.messages = messages_system

    def _message_user(self, msg: str, level: str):
        text = as_markdown(escape(msg))
        match level:
            case 'debug':
                self.messages.debug(self.request, text)
            case 'warning' | 'archive' | 'delete':
                self.messages.warning(self.request, text)
            case 'error' | 'panic':
                self.messages.error(self.request, text)
            case 'info':
                self.messages.info(self.request, text)
            case 'success' | 'insert' | 'update':
                self.messages.success(self.request, text)
            case _:
                self.messages.error(self.request, text)

    def publica(self, item: Model, msg: str, level: str, user_feedback=True):
        if not isinstance(item, Model) and not hasattr(item, 'pk'):
            raise ValueError(
                "Solo se pueden publicar en el bus"
                " instancias de clases derivadas de la clase Model"
                " de Django,"
                " o de clases que permitan el acceso a su clave primaria"
                " con el atributo ``pk``\n\n."
                " El sujeto indicado: {escape(repr(item))}"
                f" es de tipo {escape(repr(type(item)))}"
                )
        if user_feedback:
            self._message_user(msg, level)
        Evento.new(item, msg, level, self.username)

    # Public methods

    def pub_nuevo_sistema(self, sistema):
        msg = f'Añadido el sistema de información {sistema}'
        self.publica(sistema, msg, 'insert')

    def pub_sistema_modificado(self, sistema, **kwargs):
        buff = [
            f"El sistema de información {sistema}"
            " ha sido modificado:"
            ]
        for field_name, value in kwargs.items():
            buff.append(f'- {field_name} : {value!r}')
        msg = '\n\n'.join(buff)
        self.publica(sistema, msg, 'update')

    def pub_sistema_asignado_organismo(self, sistema, organismo):
        msg = (
            f'El sistema {sistema}'
            ' ha sido asignado'
            f' al organismo {organismo}'
            )
        self.publica(sistema, msg, 'update')
        self.publica(organismo, msg, 'update', user_feedback=False)

    def pub_sistema_asignado_familia(self, sistema, familia):
        msg = (
            f'El sistema {sistema}'
            ' ha sido asignado'
            ' a la familia {familia}'
            )
        self.publica(sistema, msg, 'update')

    def pub_sistema_editar_finalidad(self, sistema, finalidad: str):
        msg = (
            f"La finalidad del sistema {sistema}"
            f" ha sido actualizada a {finalidad!r}"
            )
        self.publica(sistema, msg, 'update')

    def pub_sistema_editar_codigo(self, sistema, codigo: str):
        msg = (
            f"El código del sistema {sistema}"
            f" ha sido actualizada a {codigo!r}.\n"
            " Tenga en cuenta que este cambio afecta"
            " a las dirección de la página web del sistema"
            )
        self.publica(sistema, msg, 'update')

    def pub_sistema_editar_nombre(self, sistema, nombre: str):
        msg = (
            f"El nombre del sistema {sistema}"
            f" ha sido actualizada a {nombre!r}.\n"
            )
        self.publica(sistema, msg, 'update')


    def pub_sistema_editar_url(self, sistema, url: str):
        msg = (
            f"La URL de entrada al sistema {sistema}"
            f" ha sido actualizada a {url!r}.\n"
            )
        self.publica(sistema, msg, 'update')


    def pub_sistema_editar_descripcion(self, sistema, descripcion: str):
        msg = (
            f"La descripción del sistema {sistema}"
            f" ha sido actualizada a {descripcion!r}"
            )
        self.publica(sistema, msg, 'update')

    def pub_sistema_editar_observaciones(self, sistema):
        msg = (
            "Se ha actualizado el texto de las observaciones"
            f" del sistema {sistema}"
            )
        self.publica(sistema, msg, 'update')

    def pub_sistema_asignar_responsable(self, sistema, perfil):
        msg = (
            f"El usuario {perfil.usuario}"    
            f" ha sido asignado como {perfil.get_cometido_display()}"
            f" del sistema {perfil.sistema}"
            )
        self.publica(sistema, msg, 'update')
        self.publica(perfil.usuario, msg, 'update', user_feedback=False)
    
    def pub_sistema_asignar_materia(self, sistema, materia):
        msg = (
            f"El sistema {sistema} ha sido asignado"
            f" a la materia competencial {materia}"
            )
        self.publica(sistema, msg, 'update')
    
    def pub_sistema_asignar_icono(self, sistema):
        msg = f"Se ha asignado un icono al sistema {sistema}"
        self.publica(sistema, msg, 'update')

    def pub_sistema_conmutar_campo(self, sistema, campo: str):
        valor = getattr(sistema, campo)
        desc_valor = 'verdadero' if valor else 'falso'
        msg = (
            f'El sistema {sistema} ha cambiado su valor'
            f' {campo}, ahora vale **{desc_valor}**'
            )
        self.publica(sistema, msg, 'update')

    def pub_perfil_borrado(self, perfil):
        msg = (
            f"El usuario {perfil.usuario}"    
            f" ha dejado de ser {perfil.get_cometido_display()}"
            f" del sistema {perfil.sistema}"
            )
        self.publica(perfil.sistema, msg, 'delete')
        self.publica(perfil.usuario, msg, 'update', user_feedback=False)

    def pub_nuevo_usuario(self, usuario):
        msg = f"Se ha dado de alta al usuario {usuario}"
        self.publica(usuario, msg, 'insert')

    def pub_interlocutor_asignado(self, usuario, ente):
        msg = (
            f"El usuario {usuario}"    
            " ha sido asignado como interlocutor"
            f" del ente {ente}"
            )
        self.publica(ente, msg, 'update')
        self.publica(usuario, msg, 'update', user_feedback=False)

    def pub_interlocutor_liberado(self, usuario, ente):
        msg = (
            f"El usuario {usuario}"
            " ha sido liberado del cargo de interlocutor"
            f" del ente {ente}"
            )
        self.publica(ente, msg, 'update')
        self.publica(usuario, msg, 'update', user_feedback=False)

    def pub_sistema_asignar_juriscan(self, sistema, juriscan):
        msg = (
            f"Se ha asignado la entrada Juriscán nº {juriscan}"
            f" al sistema {sistema}"
            )
        self.publica(sistema, msg, 'update')

    def pub_sistema_desasignar_juriscan(self, sistema, juriscan):
        msg = (
            f"Se ha desasingado la entrada nº {juriscan}"
            f" al sistema {sistema}"
            )
        self.publica(sistema, msg, 'update')

    ## Backlog

    def pub_alta_backlog(self, tarea):
        msg = (
            f'Se ha añadido la tarea #{tarea.pk}: {tarea.titulo}'
            f' al S.I. {tarea.sistema}'
            )
        self.publica(tarea, msg, 'insert')
        self.publica(tarea.sistema, msg, 'update', user_feedback=False)

    def pub_tarea_modificada(self, tarea):
        msg = (
            f'Se ha modificado la tarea #{tarea.pk}: {tarea.titulo}'
            f' correspondiente al S.I. {tarea.sistema}'
            )
        self.publica(tarea, msg, 'update')
        self.publica(tarea.sistema, msg, 'update', user_feedback=False)

    def pub_tarea_cerrada(self, tarea):
        msg = (
            f'Se ha cerrado la tarea #{tarea.pk}: {tarea.titulo}'
            f' correspondiente al S.I. {tarea.sistema}'
            )
        self.publica(tarea, msg, 'archive')
        self.publica(tarea.sistema, msg, 'update', user_feedback=False)
