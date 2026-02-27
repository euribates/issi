from html import escape

from django.contrib import messages
from django.conf import settings

from comun.templatetags.comun_filters import as_markdown
from antecedentes.models import HistoricoSistema
from antecedentes.models import HistoricoUsuario
from sistemas.models import Usuario
from sistemas.models import Sistema
from sistemas.models import Perfil

class Bus:

    def __init__(self, request):
        assert request.user.is_authenticated
        if settings.DEBUG:
            messages.set_level(request, messages.DEBUG)
        self.request = request
        self.usuario = Usuario.load_usuario(request.user.username)

    def _debug(self, text: str):
        messages.add_message(
            self.request,
            messages.DEBUG,
            as_markdown(text),
            extra_tags='bg-primary text-white',
            )

    def _info(self, text: str):
        messages.add_message(
            self.request,
            messages.INFO,
            as_markdown(text),
            extra_tags='bg-info',
            )

    def _success(self, text: str):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            as_markdown(text),
            extra_tags='bg-success text-white',
            )

    def _warning(self, text: str):
        messages.add_message(
            self.request,
            messages.WARNING,
            as_markdown(text),
            extra_tags='bg-warning',
            )

    def _error(self, text: str):
        messages.add_message(
            self.request,
            messages.ERROR,
            text,
            extra_tags='bg-danger text-white',
            )

    def _dispatch_message(self, msg, level):
        match level:
            case 'success':
                self._success(msg)
            case 'error':
                self._error(msg)
            case 'warning':
                self._warning(msg)
            case 'info':
                self._info(msg)
            case _:
                self._debug(msg)


    # Public methods

    def publica(self, item, msg, tipo='U', level='success'):
        self._dispatch_message(msg, level)
        _klass_name = item.__class__.__name__
        match _klass_name:
            case 'Sistema':
                HistoricoSistema(
                    sujeto=item,
                    tipo_evento=tipo,
                    descripcion=msg,
                    usuario=self.usuario,
                    ).save()
            case 'Usuario':
                HistoricoUsuario(
                    sujeto=item,
                    tipo_evento=tipo,
                    descripcion=msg,
                    usuario=self.usuario,
                    ).save()

            case _:
                raise ValueError(
                    "No se pueden publicar en el bus"
                    f" objetos de tipo {escape(_klass_name)}"
                    )

    def nuevo_sistema(self, sistema: Sistema):
        self.publica(sistema, 'I', f'Añadido el sistema de información {sistema}')

    def sistema_modificado(self, sistema: Sistema, **kwargs):
        buff = [f"El sistema de información {sistema} ha sido modificado"]
        for field_name, value in kwargs.items:
            buff.append(f'- {field_name} : {value!r}')
        msg = '\n'.join(buff)
        self.publica(sistema, 'U', msg)

    def sistema_asignado_organismo(self, sistema: Sistema, organismo):
        msg = f'El sistema {sistema} ha sido asignado al organismo {organismo}'
        self.publica(sistema, 'U', msg) 

    def sistema_asignado_familia(self, sistema: Sistema, familia):
        msg = f'El sistema {sistema} ha sido asignado a la familia {familia}'
        self.publica(sistema, 'U', msg) 

    def sistema_editar_finalidad(self, sistema: Sistema, finalidad: str):
        msg = (
            f"La finalidad del sistema {sistema}"
            f" ha sido actualizada a {finalidad!r}"
            )
        self.publica(sistema, 'U', msg) 

    def sistema_editar_descripcion(self, sistema: Sistema, descripcion: str):
        msg = (
            f"La descripción del sistema {sistema}"
            f" ha sido actualizada a {descripcion!r}"
            )
        self.publica(sistema, 'U', msg) 

    def sistema_asignar_responsable(self, sistema: Sistema, perfil: Perfil):
        msg = (
            f"El usuario {perfil.usuario}"    
            f" ha sido asignado como {perfil.get_cometido_display()}"
            f" del sistema {perfil.sistema}"
            )
        self.publica(sistema, 'U', msg) 
    
    def sistema_asignar_materia(self, sistema: Sistema, materia):
        msg = (
            f"El sistema {sistema} ha sido asignado"
            f" a la materia competencial {materia}"
            )
        self.publica(sistema, 'U', msg) 
    
    def sistema_asignar_icono(self, sistema: Sistema):
        msg = f"Se ha asignado un icono al sistema {sistema}"
        self.publica(sistema, 'U', msg) 

    def perfil_borrado(self, perfil: Perfil):
        msg = (
            f"El usuario {perfil.usuario}"    
            f" ha dejado de ser {perfil.get_cometido_display()}"
            f" del sistema {perfil.sistema}"
            )
        self.publica(perfil.sistema, 'U', msg) 

    def nuevo_usuario(self, usuario: Usuario):
        msg = f"Se ha dado de alta al usuario {usuario}"
        self.publica(usuario, 'I', msg)


