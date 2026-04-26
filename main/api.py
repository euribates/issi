#!/usr/bin/env python3

import traceback
from typing import List, Optional
from html import escape

from ninja import NinjaAPI, Schema, Form
from ninja.pagination import paginate, LimitOffsetPagination

from sistemas.models import Sistema
from sistemas.models import Tema
from sistemas.models import Arquetipo



VERSION = 'v0'

api = NinjaAPI()


@api.get('/status/')
def api_status(request):
    return {
        'version': VERSION,
        'status': 'ok',
        }
    

class OrganismoSchema(Schema):
    id_organismo: int
    nombre_organismo: str
    dir3: str
    id_sirhus: int


    

class AltaSistemaSchema(Schema):
    nombre_sistema: str
    codigo: str
    descripcion: str = ""
    finalidad: str = ""
    observaciones: str = ""
    organismo: int
    tema: str
    juriscan: List[int] = None
    responsables_funcionales: List[str] = None
    responsables_tecnologicos: List[str] = None


@api.post('/sistemas/alta/')
def alta_sistema(request, payload: Form[AltaSistemaSchema]):
    try:
        sistema = Sistema.alta_sistema(**payload.dict())
        return {
            'status': 'success',
            'result': {
                'id_sistema': sistema.pk,
                'codigo': sistema.codigo,
                'uuid_sistema': sistema.uuid_sistema,
                'created': sistema.created,
                }
            }
    except Exception as err:
        lines = traceback.format_exception(err)
        return {
            'status': 'error',
            'message': escape(str(err)),
            'traceback': lines,
            }


class ActualizarSistemaSchema(Schema):
    nombre_sistema: str = None
    finalidad: Optional[str] = None
    descripcion: Optional[str] = None
    observaciones: Optional[str] = None
    organismo: Optional[int] = None
    tema: Optional[str] = None
    juriscan: Optional[List[int]] = None
    responsables_funcionales: Optional[List[str]] = None
    responsables_tecnologicos: Optional[List[str]] = None


@api.post('/sistemas/actualizar/{id_sistema}/')
def actualizar_sistema(request, id_sistema, payload: Form[ActualizarSistemaSchema]):
    try:
        sistema = Sistema.load_sistema(id_sistema)
        arguments = {
            name: value
            for name, value in payload.dict().items()
            if value is not None
            }
        sistema.actualizar_sistema(**arguments)
        return {
            'status': 'success',
            'result': {
                'id_sistema': sistema.pk,
                'codigo': sistema.codigo,
                'uuid_sistema': str(sistema.uuid_sistema),
                'updated': sistema.updated.isoformat(),
                }
            }
    except Exception as err:
        lines = traceback.format_exception(err)
        return {
            'status': 'error',
            'message': escape(str(err)),
            'traceback': lines,
            }


class SimpleSistemaSchema(Schema):
    id_sistema: int
    nombre_sistema: str
    codigo: str


@api.get('/sistemas/', response=List[SimpleSistemaSchema])
@paginate(LimitOffsetPagination)
def api_sistemas(request):
    return Sistema.objects.all()
    

class SistemaSchema(Schema):
    id_sistema: int
    nombre_sistema: str
    codigo: str
    finalidad: str
    url: str|None
    organismo: OrganismoSchema
    

@api.get('/sistemas/{id_sistema}/', response=SistemaSchema)
def api_detalle_sistema(request, id_sistema: int):
    return Sistema.load_sistema(id_sistema)
    

class TemaSchema(Schema):
    id_tema: str
    nombre_tema: str
    transversal: bool


@api.get('/temas/', response=List[TemaSchema])
def api_temas(request):
    """Devuelve un listado de todos las áreas competenciales
    en uso.
    """
    return Tema.objects.all()


class ArquetipoSchema(Schema):
    id_arquetipo: int
    tipo: str
    espacio: str
    funcion: str
    clave: str
    descripcion: str
    
    @staticmethod
    def resolve_tipo(obj):
        return obj.tipo.pk
        
    @staticmethod
    def resolve_clave(obj):
        return str(obj)



@api.get('/arquetipos/', response=List[ArquetipoSchema])
@paginate(LimitOffsetPagination)
def api_arquetipos(request):
    return Arquetipo.objects.all()

    
