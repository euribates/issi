from typing import List

from ninja import NinjaAPI, Schema
from ninja.pagination import paginate, LimitOffsetPagination

import sistemas.models


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


    
class SimpleSistemaSchema(Schema):
    id_sistema: int
    nombre_sistema: str
    codigo: str


class SistemaSchema(Schema):
    id_sistema: int
    nombre_sistema: str
    codigo: str
    finalidad: str
    url: str|None
    organismo: OrganismoSchema
    

@api.get('/sistemas/', response=List[SimpleSistemaSchema])
@paginate(LimitOffsetPagination)
def api_sistemas(request):
    return sistemas.models.Sistema.objects.all()
    

@api.get('/sistemas/{id_sistema}/', response=SistemaSchema)
def api_detalle_sistema(request, id_sistema: int):
    return sistemas.models.Sistema.load_sistema(id_sistema)
    

class TemaSchema(Schema):
    id_tema: str
    nombre_tema: str
    transversal: bool


@api.get('/temas/', response=List[TemaSchema])
def api_temas(request):
    """Devuelve un listado de todos las áreas competenciales
    en uso.
    """
    return sistemas.models.Tema.objects.all()


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
    return sistemas.models.Arquetipo.objects.all()

    
